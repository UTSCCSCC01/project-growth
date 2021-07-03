from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .utils import get_turn_info

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
    return render(request, 'video_chat/peer.html', context=context)