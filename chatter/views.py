from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'chatter/index.html', {})

@login_required
def room(request, room_name):
    return render(request, 'chatter/room.html', {
        'room_name_json': room_name,
        'username': request.user.username,
    })