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

# Helper function to get a pretty string of main members
def get_users_string(company_obj):
    users = User.objects.filter(company=company_obj)
    result = "Members: "
    if len(users) == 0:
        result = "No member"
    elif len(users) <= 2:
        for user in users:
            result += user.username + ", "
        result = result[:-2]
    else:
        result += users[0].username + ", " + users[1].username + " and " + str(len(users)-2) + " other(s) "
    return result

# Landing page for users without a company
def companies_view(request):

    company_obj = request.user.company
    has_company =  company_obj != None
    member_list = get_users_string(company_obj)

    companies = Company.objects.all()
    companies_dict = {company_obj: get_users_string(company_obj) for company_obj in companies }

    if has_company:
        companies_dict.pop(company_obj)

    context = {
        "companies_dict": companies_dict,
        "has_company": has_company,
        "company_obj": company_obj,
        "member_list": member_list
    }
    return render(request, "company/companies.html", context)

# Page for viewing user's company
def my_company_view(request, company_id):
    company_obj = get_object_or_404(Company, id=company_id)
    users = User.objects.filter(company=company_obj)
    viewer_is_member = request.user in users
    print(viewer_is_member)

    context = {
        "company_obj": company_obj,
        'users': users,
        "viewer_is_member": viewer_is_member
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
    users_existing = User.objects.filter(company=company_obj)

    print(request.method)

    if request.method == "POST":
        # Confirming deletion
        company_obj.delete()
        return redirect("../../")

    context = {
        "company_obj": company_obj,
        "users_existing": users_existing
    }
    return render(request, "company/delete_company.html", context)

# Page for company owners to edit their company
def manage_users_view(request, company_id):

    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # When posting the form
    if request.method == "POST":
        # if request.GET.get.action
        print(request.GET.get)
        if "add_user" in request.POST:

            # Add new user to company
            userid = request.POST.get('user_to_add')
            new_user = User.objects.get(id=userid)
            company_obj.user_set.add(new_user)

        elif "remove_user" in request.POST:
            # Remove existing users form company
            userid = request.POST.get('user_to_remove')
            user_to_remove = User.objects.get(id=userid)
            company_obj.user_set.remove(user_to_remove)

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
        users_available = User.objects.filter(company=None)
        users_existing = User.objects.filter(company=company_obj)

        context = {
            'users_available': users_available,
            'company_obj': company_obj,
            'users_existing': users_existing
        }
        return render(request, 'company/manage_users.html', context)


def add_current_user_view(request, company_id):

    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # When posting the form
    if request.method == "POST":
        # if request.GET.get.action
        print(request.GET.get)
        if "add_user" in request.POST:

            # Add new user to company
            new_user = request.user
            company_obj.user_set.add(new_user)


        return redirect('my_company' , company_id=company_id)



    # When just viewing the form
    else:
        has_company = request.user.company != None

        context = {
            'company_obj': company_obj,
            "has_company":has_company
        }
        return render(request, 'company/add_current_user.html', context)

        # form = ModifyCompanyForm(instance=company_obj)
        # context = {
        #     "company_obj": company_obj,
        #     'form' : form
        # }
        # return render(request, "company/modify_company.html", context)