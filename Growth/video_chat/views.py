from django.shortcuts import render

from .utils import get_turn_info

def peerB(request):
    # get numb turn info
    context = get_turn_info()

    return render(request, 'video_chat/peerB.html', context=context)

def peerA(request):
    # get numb turn info
    context = get_turn_info()

    return render(request, 'video_chat/peerA.html', context=context)

def peer(request):
    # get numb turn info
    context = get_turn_info()
    #print('context: ', context)

    return render(request, 'video_chat/peer.html', context=context)