from django.shortcuts import render
from django.http import  HttpResponse

# Create your views here.
def add_company_view(request, *args, **kwargs):
    user = request.user
    print(user)
    return render(request, "company/add_company.html", {})
    #return HttpResponse("<h1>Add Company</h>") # String of HTML code

def modify_company_view(request, *args, **kwargs):
    user = request.user
    # TODO: replace with company db
    my_company = {
        "name": "Red Purple",
        "size": "0-3 employees",
        "founders": ["Ethan", "Diana"]
    }
    return render(request, "company/modify_company.html", my_company)
