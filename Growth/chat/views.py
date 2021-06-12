from django.shortcuts import render
from json import dumps

from django.contrib.auth.decorators import login_required


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
