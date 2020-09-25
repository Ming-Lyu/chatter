# -*- coding: utf-8 -*-

from django.contrib import admin
from chatter.models import Dialog, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 1

@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline
    ]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass