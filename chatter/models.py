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
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery
from django.conf import settings

User = get_user_model()

def get_official_user():
    # `get_or_create` just for testing purpose
    user, _ = User.objects.get_or_create(username=settings.OFFICIAL_USER) 
    return user

class DialogQuerySet(models.QuerySet):

    def get_or_create_dialog(self, owner:User, *, opponent:User = None, title:str='', id:int=None) -> 'Dialog':
        '''If opponent is not defined, then we assumpt that is the official user
        '''
        if opponent is None:
            opponent = get_official_user()
        try:
            if id:
                dialog = self.get(pk=id)
            else:
                if owner!=opponent:
                    dialog = self.filter(participants=owner).filter(participants=opponent).get()
                else: # chat with self
                    dialog = self.exclude(participants__in=User.objects.exclude(pk=owner.pk).values_list('id', flat=True)).filter(participants=owner).get()
        except ObjectDoesNotExist:
            dialog = self.create(title=title)
            dialog.participants.add(owner, opponent)
        return dialog

    def latest_message_list(self):
        '''A list of dialogs with newest message attached
        '''
        latest_messages = Message.objects.filter(dialog=OuterRef('pk')).order_by('-created')
        return self.annotate(last_message=Subquery(latest_messages.values('content')[:1]))
    

class MessageQuerySet(models.QuerySet):

    def get_queryset(self):
        return self.filter(is_removed=False)

class Dialog(TimeStampedModel):
    # TODO verbalization
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_("participants"))
    title    = models.CharField(max_length=100, blank=True, null=True)

    # customized manager
    objects = DialogQuerySet.as_manager()

    def __str__(self):
        return _(f"dialog-{self.pk}")

from django.core.validators import FileExtensionValidator



class Message(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"),
                              on_delete=models.CASCADE)
    # title  = models.CharField(max_length=100)
    content   = RichTextField()
    workflow_state = FSMField(default='sended')
    
    # support message deletion
    is_removed = models.BooleanField(default=False, blank=True)
    # attached to one dialog
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages')
    file =  models.FileField(upload_to='files/', validators=[FileExtensionValidator(
        allowed_extensions=['pdf', 'png', 'jpg', 'jpeg'])], null=True)

    def __str__(self):
        return _(f"{self.owner}'s message")
        
    objects = models.Manager()
    available_objects = MessageQuerySet.as_manager()
    # @transition(field=workflow_state, source='deleted', target='sended')
    # def send(self):
    #     pass

    @transition(field=workflow_state, source='sended', target='deleted')
    def withdrawl(self):
        pass


    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_removed`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_removed = True
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)