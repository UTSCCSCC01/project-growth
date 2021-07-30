from django.shortcuts import render
from json import dumps

from django.contrib.auth.decorators import login_required


from .utils import get_turn_info



@login_required
def entryChat(request):
    return render(request, 'chat/entryChat.html', {})

@login_required
def room(request, room_name):
    # create data dictionary
   # dic = {
    #'username' : self.request.user
    #}
    #dataJSON = dumps(dic)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
    #    'username' : dataJSON
    })

@login_required
def peerB(request):
    # get numb turn info
    context = get_turn_info()

    return render(request, 'video_chat/peerB.html', context=context)

@login_required
def peerA(request):
    # get numb turn info
    context = get_turn_info()

    return render(request, 'video_chat/peerA.html', context=context)

@login_required
def peer(request):
    # get numb turn info
    context = get_turn_info()
    #print('context: ', context)
    return render(request, 'video_chat/peer.html', {
        'room_name': room_name,
        },context=context)
