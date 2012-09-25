#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

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

class SnippetAdmin(admin.ModelAdmin):
    list_display = ['text', 'author']
    list_filter = ['created']

#admin register

admin.site.register(Snippet, SnippetAdmin)