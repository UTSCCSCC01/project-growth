from django.shortcuts import render
from django.http import  HttpResponse

# Create your views here.
def add_company_view(request, *args, **kwargs):
    user = request.user
    print(user)
    return HttpResponse("<h1>Add Company</h>") # String of HTML code

def modify_company_view(request, *args, **kwargs):
    user = request.user
    return HttpResponse("<h1>Modify Company</h>") # String of HTML code