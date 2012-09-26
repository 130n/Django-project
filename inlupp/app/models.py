#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=80, default=80*'o')

class Friendship(models.Model):
    user =models.ForeignKey(User, related_name='me')
    friend =models.ForeignKey(User,related_name='you')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Friendship'
        verbose_name_plural = 'Friendships'

    def __unicode__(self):
        return unicode(self.user) + " - " + unicode(self.friend)
    

class Story(models.Model):
    LENGTH_CHOICES=(
        (2500,"Page"),
        (10000,"Short"),
        (100000,"Novella"),
    )
    CATEGORY=(
        ('Humor','Funny and weird'),
        ('Horror','Scary and Creepy'),
        ('Erotica', 'Sex, Love and Smut'),
        ('Scifi/Fantasy','Space and Sorcery'),
        ('Biographical','Reality and You'),
    )
    AVAILABLE_TO=(
        ("Public","Public to read and write"),
        ("Private","Public to read, only friends can write"),
        ("PrivateEX","Only friends can read and write"),
    )
    STORY_LANGUAGES = (
        ('Sve','Svenska'),
        ('Eng','English'),
        )
    title = models.CharField(max_length=80)
    length = models.IntegerField(choices=LENGTH_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    availability = models.CharField(max_length=9,choices=AVAILABLE_TO)
    language=models.CharField(max_length=3,choices=STORY_LANGUAGES)

    class Meta:
        verbose_name = _('Story')
        verbose_name_plural = _('Storys')

    def __unicode__(self):
        return unicode(self.creator) + " - " + unicode(self.title)
    

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, blank=True, null=True)
    text = models.TextField(max_length=1)


    class Meta:
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippets'

    def __unicode__(self):
        return unicode(self.author) + " - " + unicode(self.text)


# Admin

class FriendshipAdmin(admin.ModelAdmin):
    pass

class StoryAdmin(admin.ModelAdmin):
    pass

class SnippetAdmin(admin.ModelAdmin):
    list_display = ['text', 'author']
    list_filter = ['created']

#admin register

admin.site.register(Snippet, SnippetAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Story, StoryAdmin)