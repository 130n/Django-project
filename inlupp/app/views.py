#!/usr/bin/python
# -*- coding: utf-8 -*-
# Create your views here.
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext

from app.models import Snippet, Story
from app.forms import LoginForm, RegForm, SnippetForm, StoryForm

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    elem = {
        'title':'Login',
    }

    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        loginAuth(request)
        if loginform.is_valid():
            return HttpResponseRedirect('/home/')
        else:
            elem.update({'error':'inloggning misslyckades'})
            return render_to_response("login.html",elem,context_instance=RequestContext(request))
    # elem.update(csrf(request))
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
            print "disabled account"
    else:
        print "login failed"

def register(request):
    reg_form = RegForm()
    if request.method == 'POST':
        reg_new(request)
    elem = {
        'title':'Registrering',
        'reg_form':reg_form,
    }
    elem.update(csrf(request))
    return render_to_response("register.html",elem)

def reg_new(request):
    exist = User.objects.filter(username=request.POST['username'])
    if (request.POST['password']==request.POST['confirm_password']) and not exist.exists():
        username=request.POST['username']
        password=request.POST['password']
        User.objects.create_user(username,None,password)
        home(request)

    else:
        print "user already exists"

def newsnip(request):
    elem= {
    'title':'New Snippet',
    'content':'waaaaah',
    }
    if request.method=='POST':
        snip_form=SnippetForm(request.POST)
        elem.update({'snip_form':snip_form,})

        if snip_form.is_valid():
            print snip_form.cleaned_data
            newsnip=Snippet(created=datetime.datetime.now(),author=request.user,text=request.POST['text'])
            newsnip.save()
            print newsnip
            return HttpResponseRedirect('/home')
        else:
            print "invalid snip_form"
    else:
        snip_form=SnippetForm()
        elem.update({'snip_form':snip_form,})
        return render_to_response("newsnip.html",elem,context_instance=RequestContext(request))

def newstory(request):
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
            print newsnip
            return HttpResponseRedirect('/home')
        else:
            print "invalid story_form"
    else:
        story_form=StoryForm()
        elem.update({'story_form':story_form,})
    return render_to_response("newstory.html",elem,context_instance=RequestContext(request))


def home(request):
    elem = {
        'title':'Home',
        'content':"Inloggad!",
        'user':request.user ,
    }
    if request.method=='POST':
        story_form = StoryForm(request.POST)
        elem.update({'story_form':story_form,})
        #handle
    else:
        story_form = StoryForm()
        elem.update({'story_form':story_form,})
    if request.user.is_authenticated():
        return render_to_response("home.html",elem,context_instance=RequestContext(request))
    else:
        return render_to_response("home.html",{'title':"FAILED LOGIN!",'content':"FAILED LOGIN!"},context_instance=RequestContext(request))