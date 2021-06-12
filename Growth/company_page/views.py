from django.shortcuts import render, get_object_or_404, redirect
from django.http import  HttpResponse
from .models import Company
from .forms import AddCompanyForm, ModifyCompanyForm
import os
# Create your views here.

magic_id = 4

def my_company_view(request, *args, **kwargs):
    user = request.user

    try:
        # TODO: Change to real find object
        company_obj = Company.objects.get(id=magic_id)
    except:
        # TODO: Elegantize this
        context = {
            "company_obj": None
        }
    else:
        context = {
            "company_obj": company_obj,
            "founders": ["Ethan", "Diana"] # TODO: Change to real founders
        }
    return render(request, "company/my_company.html", context)

def add_company_view(request, *args, **kwargs):
    form = AddCompanyForm(request.POST or None, request.FILES)

    if form.is_valid():
        form.save()
        form = ModifyCompanyForm

    context = {
        'form' : form
    }

    return render(request, "company/add_company.html", context)
    #return HttpResponse("<h1>Add Company</h>") # String of HTML code

def modify_company_view(request, *args, **kwargs):
    # user = request.user
    # try:
    #     # TODO: Change to real find object
    #     company_obj = Company.objects.get(id=1)
    # except:
    #     # TODO: Elegantize this
    #     context = {
    #         "company_obj": None
    #     }
    # else:
    #     context = {
    #         "company_obj": company_obj,
    #         "founders": ["Ethan", "Diana"] # TODO: Change to real founders
    #     }
    company_obj = get_object_or_404(Company, id = magic_id)
    # Old img path
    old_image_path = company_obj.logo.path

    #company_obj = Company.objects.get(id=magic_id)
    if request.method == "POST":
        form = ModifyCompanyForm(request.POST or None, request.FILES, instance=company_obj)
        if form.is_valid():

            # # deleting old uploaded image.

            new_image_path = company_obj.logo.path
            if os.path.exists(old_image_path) and old_image_path != new_image_path:
                os.remove(old_image_path)

            form.save()
            return redirect('company/my_company.html')
    else:


        form = ModifyCompanyForm( instance=company_obj)
    context = {
        "company_obj": company_obj,
        'form' : form
    }
    return render(request, "company/modify_company.html", context)

