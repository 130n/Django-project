#!/usr/bin/python
# -*- coding: utf-8 -*-
# Leon Hennings 880827-0154
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect
# from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from app.models import Snippet, Story, UserProfile, Friendship
from app.forms import LoginForm, RegForm, SnippetForm, StoryForm

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    elem = {
        'title':'Login',
    }
    #inloggade användare behöver inte se login view
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        loginAuth(request)
        if loginform.is_valid():
            if request.user.is_authenticated():
                #endast för admin, som saknar user profile från början, underlättar testning
                up = UserProfile.objects.filter(user=request.user)
                if not up.exists():
                    new_profile = UserProfile(user=request.user, description=16*"admin")
                    new_profile.save()
                return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('')    
            loginform = LoginForm()
            elem.update({'error':'inloggning misslyckades','login_form':loginform})
            print "aha"
            return render_to_response("login.html",elem,context_instance=RequestContext(request))
    else:
        loginform = LoginForm()
    elem.update({'login_form':loginform})
    return render_to_response("login.html",elem,context_instance=RequestContext(request))
    
def loginAuth(request):
    username=request.POST['username']
    password=request.POST['password']
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            print "uname and pw checks out"
            login(request, user)
            print "login ok"
        else:
            login(request, user)
            print "disabled account"
    else:
        print "login failed"

def register(request):
    reg_form = RegForm()
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        reg_new(request)
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home/')
    else:
        elem = {
            'title':'Registrering',
            'reg_form':reg_form,
        }
        return render_to_response("register.html",elem,context_instance=RequestContext(request))

def reg_new(request):
    exist = User.objects.filter(username=request.POST['username'])
    if (request.POST['password']==request.POST['confirm_password']) and not exist.exists():
        print request.POST
        username=request.POST['username']
        password=request.POST['password']
        description=request.POST['description']
        u=User.objects.create_user(username,None,password)
        fill=80-len(description)
        if fill==80:
            usr_desc=UserProfile(user=u)
        else:
            for x in range(0,fill):
                description+="="
            usr_desc=UserProfile(user=u,description=description)
        usr_desc.save()
        loginAuth(request)

    else:
        print "user already exists"


def newstory(request):
    if request.user.is_authenticated():
        elem= {
        'title':'Ny Story',
        'content':'waaaaah2',
        }
        if request.method=='POST':
            story_form=StoryForm(request.POST)
            elem.update({'story_form':story_form,})

            if story_form.is_valid():
                print story_form.cleaned_data
                title = request.POST['title']
                length = request.POST['length']
                availability = request.POST['availability']
                language=request.POST['language']

                newstory=Story(created=datetime.datetime.now(),creator=request.user,title=title,length=length,availability=availability,language=language)
                newstory.save()
                return HttpResponseRedirect('/home')
            else:
                print "invalid story_form"
        else:
            story_form=StoryForm()
            elem.update({'story_form':story_form,})
        return render_to_response("newstory.html",elem,context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")


def home(request, next=0):
    prev_page=0
    if next>0:
        prev_page = int(next)-1
    next_page = int(next)+1

    stories = Story.objects.filter(availability="Public" or "Private").order_by('-created')[(next_page-1)*10:(next_page-1)*10+9]
    # .order_by('created')
    # [:1]
    # paginator = Paginator(stories, 25)
    elem = {
        'title':'Home',
        'content':"Inloggad!",
        'user':request.user ,
        'stories':stories,
        'next_page':next_page,
        'prev_page':prev_page,
    }
    if request.method=='POST':
        pass
    else:
        pass
    if request.user.is_authenticated():
        return render_to_response("home.html",elem,context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")


def profile(request,userID):
    if request.user.is_authenticated():
        userdata=User.objects.get(id=userID)
        profile=UserProfile.objects.get(user=userdata)
        not_friend = not Friendship.objects.filter(user=request.user,friend=userdata).exists()
        if request.method=='POST':
            print "post!"
            new_relationship = Friendship(created=datetime.datetime.now(),user=request.user,friend=userdata)
            new_relationship.save()
            not_friend = False
        elem={
            'title':userdata.username+"s profil",
            'userdata':userdata,
            'profile':profile,
            'userID':userID,
            'not_friend':not_friend,
        }
        return render_to_response("profile.html",elem,context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

def story(request,storyID):
    if request.user.is_authenticated():
        story = Story.objects.get(id=storyID)
        new_sequence = Snippet.objects.filter(story=story).count()+1
        already_taken = Snippet.objects.filter(story=story,sequence=new_sequence)

        if already_taken:
            print "finns redan"
            return HttpResponseRedirect('')

        snippets = Snippet.objects.filter(story=story)
        snip_form=SnippetForm()
        elem= {
            'title':story.title,
            'story':story,
            'snippets':snippets,
            'snip_form':snip_form,
        }
        if request.method=='POST':
                snip_form=SnippetForm(request.POST)
                elem.update({'snip_form':snip_form,})
                if snip_form.is_valid():
                    print snip_form.cleaned_data
                    newsnip=Snippet(created=datetime.datetime.now(),author=request.user,text=request.POST['text'],story=story,sequence=new_sequence)
                    newsnip.save()
                    return HttpResponseRedirect('')
                else:
                    elem.update({'error':"invalid snippetform"})
                    return render_to_response("newsnip.html",elem,context_instance=RequestContext(request))
        else:
            snip_form=SnippetForm()
            elem.update({'snip_form':snip_form,})
            return render_to_response("newsnip.html",elem,context_instance=RequestContext(request))
        return render_to_response("newsnip.html",elem,context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

def friends(request):
    if request.user.is_authenticated():
        friends = [friendship.friend for friendship in request.user.me.all()]
        elem= {
            'title':'Dina vänner',
            'friends':friends,
        }
        return render_to_response("friends.html",elem,context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")