# -*- coding: utf-8 -*-
from .utils.models import TimeStampedModel
from django.utils.translation import ugettext as _
from django.utils.timezone import localtime
from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django_fsm import FSMField, transition
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

def get_official_user():
    # `get_or_create` just for testing purpose
    user, _ = User.objects.get_or_create(username='official_user') 
    return user


class DialogQuerySet(models.QuerySet):

    def get_or_create_dialog(self, owner:User, *, opponent:User = None, title:str='') -> 'Dialog':
        '''If opponent is not defined, then we assumpt that is the official user
        '''
        if opponent is None:
            opponent = get_official_user()
        try:
            dialog = self.filter(participants=owner).filter(participants=opponent).get()
        except ObjectDoesNotExist:
            dialog = self.create(title=title)
            dialog.participants.add(owner, opponent)
        return dialog


class Dialog(TimeStampedModel):
    # TODO verbalization
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("participants"))
    title    = models.CharField(max_length=100, blank=True, null=True)

    # customized manager
    objects = DialogQuerySet.as_manager()

    def __str__(self):
        return _(f"dialog-{self.pk}")


class Message(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"),
                              on_delete=models.CASCADE)
    # title  = models.CharField(max_length=100)
    content   = RichTextField()
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
