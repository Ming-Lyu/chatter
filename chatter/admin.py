# -*- coding: utf-8 -*-

from django.contrib import admin
from chatter.models import Dialog

@admin.register(Dialog)
class AuthorAdmin(admin.ModelAdmin):
    pass

