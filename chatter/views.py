from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


import json

from chatter.models import Dialog

def index(request):
    return render(request, 'chatter/index.html', {})

@login_required
def room(request, room_name):
    #init
    dialog_users = User.objects.filter(id__in=Dialog.objects.filter(participants__id=1).values_list('participants', flat=True))

    return render(request, 'chatter/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
        'dialog_users': dialog_users
    })