from django.shortcuts import render
from django.http import  HttpResponse

# Create your views here.
def add_company_view(*args, **kwargs):
    return HttpResponse("<h1>Add Company</h>") # String of HTML code