#!/usr/bin/python
# -*- coding: utf-8 -*-
#FORMS

from django import forms
from django.forms import ModelForm
from app.models import Snippet, Story
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Your Password")

class RegForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Your Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Repeat")

class SnippetForm(ModelForm):
    class Meta:
        model = Snippet

class StoryForm(ModelForm):
	class Meta:
		model = Story
		exclude =('creator',)

