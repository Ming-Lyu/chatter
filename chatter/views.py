from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


import json

from chatter.models import Dialog

def index(request):
    return render(request, 'chatter/index.html', {})

@login_required
def room(request, room_pk=None):
    opponent = request.GET.get('opponent', None)
    if opponent:
        opponent = User.objects.get(username=opponent)

    dialog = Dialog.objects.get_or_create_dialog(request.user, opponent=opponent, id=room_pk)

    #init
    id_list = [user.pk for dialog in Dialog.objects.filter(participants=request.user).iterator() for user in dialog.participants.all()]
    dialog_users = User.objects.filter(id__in=id_list)
    
    # TODO this work only 1 on 1
    opponent_username = opponent if opponent else dialog.participants.exclude(pk = request.user.pk).get().username

    return render(request, 'chatter/room.html', {
        'room_pk_json': mark_safe(json.dumps(dialog.pk)),
        'username': mark_safe(json.dumps(request.user.username)),
        'dialog_users': dialog_users,
        'opponent_username': opponent_username,
    })