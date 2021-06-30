from django.shortcuts import render, get_object_or_404, redirect
from users.models import User

from .models import Company
from .forms import AddCompanyForm, ModifyCompanyForm
from django.contrib import messages
import os


# Redirect user to their company, or show show_company_view if they don't have one
def redirect_company(request):
    if request.user.company:
        # get your models
        company_id = request.user.company.id
        return redirect('my_company', company_id=company_id)

    else:
        return redirect('no_company')



# Landing page for users without a company
def no_company_view(request):
    return render(request, "company/no_company.html")

# Page for viewing user's company
def my_company_view(request, company_id):
    #user = request.user
    company_obj = get_object_or_404(Company, id=company_id)
    context = {
        "company_obj": company_obj,
        "founders": ["Ethan", "Diana"] # TODO: Change to real founders
    }
    return render(request, "company/my_company.html", context)

# Page for adding a new company
def add_company_view(request):
    form = AddCompanyForm()
    if request.method == "POST":

        # Check for existing company
        if request.user.company:
            # Return alert message
            messages.error(request, "You already have a company!")

        else:

            form = AddCompanyForm(request.POST or None, request.FILES)

    # Check if the form is valid, if so, get the new object id and save it
    if form.is_valid():
        new_company = form.save()


        new_company.user_set.add(request.user)

        #request.user.
        # Go back to company page while passing the new id
        return redirect('my_company' , company_id=new_company.id)


    # If the form is not valid, re-run the form
    context = {
        'form' : form
    }

    return render(request, "company/add_company.html", context)

# Page for company owners to edit their company
def modify_company_view(request, company_id):

    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # Record the old img path to remove it later just in case the logo is updated
    old_image_path = company_obj.logo.path

    # When posting the form
    if request.method == "POST":

        form = ModifyCompanyForm(request.POST or None, request.FILES, instance=company_obj)
        if form.is_valid():

            # deleting old uploaded logo image.
            new_image_path = company_obj.logo.path
            if os.path.exists(old_image_path) and old_image_path != new_image_path:
                os.remove(old_image_path)

            # Save the new form
            form.save()
            return redirect('my_company', company_id=company_id)

    # When just viewing the form
    else:
        form = ModifyCompanyForm(instance=company_obj)
        context = {
            "company_obj": company_obj,
            'form' : form
        }
        return render(request, "company/modify_company.html", context)

def delete_company_view(request, company_id):
    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)
    print(request.method)

    if request.method == "POST":
        # Confirming deletion
        company_obj.delete()
        return redirect("../../")

    context = {
        "company_obj": company_obj
    }
    return render(request, "company/delete_company.html", context)

# Page for company owners to edit their company
def add_other_user(request, company_id):

    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # When posting the form
    if request.method == "POST":
        users = User.objects.filter(company=None)
        users = User.objects.all()

        userid = request.POST.get('user_to_add')
        # TODO: DO something with the selected user
        #context = {'users ': users}
        print("selection: " + userid)
        new_user = User.objects.get(id=userid)
        company_obj.user_set.add(new_user)

        return redirect('my_company' , company_id=company_id)

        # form = ModifyCompanyForm(request.POST or None, request.FILES, instance=company_obj)
        # if form.is_valid():
        #
        #     # deleting old uploaded logo image.
        #     new_image_path = company_obj.logo.path
        #     if os.path.exists(old_image_path) and old_image_path != new_image_path:
        #         os.remove(old_image_path)
        #
        #     # Save the new form
        #     form.save()
        #     return redirect('my_company', company_id=company_id)

    # When just viewing the form
    else:
        users = User.objects.filter(company=None)
        print(users)
        context = {
            'users': users,
            'company_obj': company_obj,
            'user1':request.user
        }
        return render(request, 'company/add_user_to_company.html', context)

        # form = ModifyCompanyForm(instance=company_obj)
        # context = {
        #     "company_obj": company_obj,
        #     'form' : form
        # }
        # return render(request, "company/modify_company.html", context)