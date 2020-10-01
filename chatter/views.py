from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User


import json

from chatter.models import Dialog
from chatter.utils.models_functions import Concat

def index(request):
    return render(request, 'chatter/index.html', {})


from .forms import MessageForm

@login_required
def room(request, room_pk=None):
    opponent = request.GET.get('opponent', None)
    if opponent:
        opponent = User.objects.get(username=opponent)

    dialog = Dialog.objects.get_or_create_dialog(request.user, opponent=opponent, id=room_pk)

    #init
    dialog_users = Dialog.objects.annotate(users = Concat('participants__username')).filter(participants=request.user).latest_message_list().values('users', 'last_message')
    for dialog_user in dialog_users:
        if not dialog_user['last_message']:
            dialog_user['last_message'] = ''
        if len(dialog_user['users'].split(',')) != 1:
            users_list = dialog_user['users'].split(',')
            users_list.remove(request.user.username)
            dialog_user['users'] = users_list[0]

    # TODO this work only 1 on 1
    opponent_username = opponent if opponent else dialog.participants.exclude(pk = request.user.pk).get().username
    message_form = MessageForm()

    return render(request, 'chatter/room.html', {
        'form': message_form,
        'room_pk_json': mark_safe(json.dumps(dialog.pk)),
        'username': mark_safe(json.dumps(request.user.username)),
        'dialog_users': dialog_users,
        'opponent_username': opponent_username,
    })