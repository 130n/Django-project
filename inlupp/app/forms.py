#!/usr/bin/python
# -*- coding: utf-8 -*-
# Leon Hennings 880827-0154
#FORMS
from django import forms
from django.forms import ModelForm
from app.models import Snippet, Story, Friendship
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class RegForm(forms.Form):
    username = forms.CharField(max_length=100)
    mail = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, label="Your Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Repeat")
    description=forms.CharField(max_length=80,required=False)

class SnippetForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='Skriv snippet: ',max_length=300)
    class Meta:
        model = Snippet
        exclude =('story','sequence','author')

class StoryForm(ModelForm):
	class Meta:
		model = Story
		exclude =('creator','availability')
