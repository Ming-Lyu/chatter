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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"),
                              on_delete=models.CASCADE)
    title  = models.CharField(max_length=100)
    body   = RichTextField()
    workflow_state = FSMField(default='draft')
    
    def __str__(self):
        return _(f"{self.owner}'s dialog")
