from django.shortcuts import render

# Create your views here.
def entryChat(request):
    return render(request, 'chat/entryChat.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def room_design(request, room_name):
    return render(request, 'chat/chatroom.css', {})