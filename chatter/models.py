# -*- coding: utf-8 -*-
from .utils.models import TimeStampedModel
from django.utils.translation import ugettext as _
from django.utils.timezone import localtime
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django_fsm import FSMField, transition


class Dialog(TimeStampedModel):
    # TODO verbalization
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("participants"))
    title  = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return _(f"dialog-{self.pk}")


class Message(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"),
                              on_delete=models.CASCADE)
    title  = models.CharField(max_length=100)
    body   = RichTextField()
    workflow_state = FSMField(default='draft')

    # attached to one dialog
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)

    def __str__(self):
        return _(f"{self.owner}'s message")

    
    @transition(field=workflow_state, source='draft', target='sended')
    def send(self):
        pass

    @transition(field=workflow_state, source='sended', target='draft')
    def withdrawl(self):
        pass
