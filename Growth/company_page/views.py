from django.shortcuts import render, get_object_or_404, redirect

from users.models import User
from .models import Company

from .forms import AddCompanyForm, ModifyCompanyForm
from django.contrib import messages
import os


# Redirect user to their company, or show show_company_view if they don't have one
def redirect_company(request):
    # If user has company
    if request.user.company:
        # get current user's company
        company_id = request.user.company.id
        return redirect('company_profile', company_id=company_id)
    # If user does not have a company
    else:
        return redirect('no_company')


# Display current user company and company list page
def companies_view(request):

    # Get current user's company
    company_obj = request.user.company
    has_company =  company_obj != None #True if user has company, false otherwise
    member_list = get_users_string(company_obj) #Get "members: xxx, xxx" string

    # Get all companies
    companies = Company.objects.all()
    # Get "members: xxx, xxx" string and map it into a dictionary
    companies_dict = {company_obj: get_users_string(company_obj) for company_obj in companies }

    if has_company:
        companies_dict.pop(company_obj)

    context = {
        "companies_dict": companies_dict, # ALl companies
        "has_company": has_company, # Current user has company or no
        "company_obj": company_obj, # Current user's company
        "member_list": member_list # Current user's company's members
    }
    return render(request, "company/companies.html", context)


# Page for viewing user's company
def company_profile_view(request, company_id):

    # Get company obj
    company_obj = get_object_or_404(Company, id=company_id)
    # Get users list
    admins, members = get_users(company_obj)["admins"], get_users(company_obj)["members"]

    # True if current viewer is company member
    viewer_is_admin = request.user in admins
    viewer_is_member = request.user in members

    # When Leave this company button is pressed
    if "leave_this_company" in request.POST:

        #  Additional step, check if there's more admin left
        if viewer_is_admin and len(admins) < 2:  # If it is not the last admin
            # Don't do anything and raise this error message
            messages.error(request, "Cannot remove the last admin!")

        else:
            # Remove existing admin/member from company
            user_to_remove = request.user  # User obj of user member to be removed

            user_to_remove.company_role = "member"  # Set role back to member
            user_to_remove.save()

            company_obj.user_set.remove(user_to_remove)  # Remove this user in User model's foreign key column
            return redirect('company_profile', company_id=company_id)

    context = {
        "company_obj": company_obj, # Target company obj
        'admins': admins, # Company company admin list
        'members': members, # Company company list
        "viewer_is_admin": viewer_is_admin, # True if current viewer is admin
        "viewer_is_member": viewer_is_member # True if current viewer is member
    }
    return render(request, "company/company_profile.html", context)


# Page for adding a new company
def add_company_view(request):

    # Initiate Django form
    form = AddCompanyForm()
    if request.method == "POST":

        # Check if viewer is already a member of other company
        if request.user.company:
            # Return alert message
            messages.error(request, "You already have a company!")
        # Otherwise, generate form
        else:
            form = AddCompanyForm(request.POST or None, request.FILES)

    # Check if the form is valid, if so, get the new object id and save it
    if form.is_valid():
        new_company = form.save() # Get django generated obj from form completion
        new_company.user_set.add(request.user) # Add current user to company

        # When success, go back to company page while passing the new id
        return redirect('company_profile' , company_id=new_company.id)


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
            if os.path.exists(old_image_path) and old_image_path != new_image_path: # True if logo is updated
                os.remove(old_image_path)

            # Save the new form
            form.save()
            # Redirect to company profile page for edited company
            return redirect('company_profile', company_id=company_id)

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
    # users_existing = User.objects.filter(company=company_obj)
    admins = get_users(company_obj)['admins']
    members = get_users(company_obj)['members']

    if request.method == "POST": # Run after user press "Confirm" button on deletion page
        # Confirming deletion
        company_obj.delete()
        return redirect("../")

    context = {
        "company_obj": company_obj,
        "admins": admins, # Members in the company that will be affected by this action
        "members": members # Members in the company that will be affected by this action
    }
    return render(request, "company/delete_company.html", context)


# Page for company owners to manage company members
def manage_users_view(request, company_id):

    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)
    # Users that do not have a company yet and is available
    users_available = User.objects.filter(company=None)
    # Current members in the company
    admins, members = get_users(company_obj)["admins"], get_users(company_obj)["members"]
    # True if user is admin (can see this page)
    is_admin = request.user in admins

    # When posting the form
    if request.method == "POST":

        # When "Add" Button is pressed on manage member page
        if "add_user" in request.POST:

            # Add new user to company
            userId = request.POST.get('user_to_add') # UserId of user member to be added
            new_user = User.objects.get(id=userId) # User obj of user member to be added
            company_obj.user_set.add(new_user) # Add this user in User model's foreign key column

        # When Remove (admin) button is pressed
        elif "remove_admin" in request.POST:

            # TODO: Additional step, check if there's more admin left
            if len(admins) >= 2: # If it is not the last admin

                # Remove existing admin from company
                userId = request.POST.get('user_to_remove') # UserId of user member to be removed
                user_to_remove = User.objects.get(id=userId) # User obj of user member to be removed

                user_to_remove.company_role = "member" # Set role back to member
                user_to_remove.save()

                company_obj.user_set.remove(user_to_remove)  # Remove this user in User model's foreign key column
            else:
                # Don't do anything and raise this error message
                messages.error(request, "Cannot remove the last admin!")

        # When Remove (member) button is pressed
        elif "remove_member" in request.POST:

            # Remove existing users form company
            userId = request.POST.get('user_to_remove') # UserId of user member to be removed
            user_to_remove = User.objects.get(id=userId) # User obj of user member to be removed

            user_to_remove.company_role = "member" # TODO： MAKE it work
            user_to_remove.save()
            company_obj.user_set.remove(user_to_remove)  # Remove this user in User model's foreign key column

        # When set_as_member (admin) button is pressed
        elif "set_as_member" in request.POST:

            # Additional step, check if there's more admin left
            if len(admins) >= 2: # If it is not the last admin

                # Get the admin object
                userId = request.POST.get('user_to_remove') # UserId of user member to be removed
                user_to_remove = User.objects.get(id=userId) # User obj of user member to be removed

                user_to_remove.company_role = "member" # Set role back to member
                user_to_remove.save()

            else:
                # Don't do anything and raise this error message
                messages.error(request, "Cannot set the last admin to member!")

        # When set_as_admin (member) button is pressed
        elif "set_as_admin" in request.POST:

            userId = request.POST.get('user_to_remove')  # UserId of user member to be removed
            user = User.objects.get(id=userId)  # User obj of user member to be removed

            user.company_role = "admin"  # Set role back to member
            user.save()

        # On success, go back to company profile page
        return redirect('manage_users' , company_id=company_id)

    # When just viewing the form
    else:

        context = {
            'users_available': users_available,
            'company_obj': company_obj,
            'admins': admins,
            'members': members,
            'is_admin': is_admin # True if user is a valid admin for this page
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

        return redirect('company_profile' , company_id=company_id)

    # When just viewing the form
    else:
        has_company = request.user.company != None

        context = {
            'company_obj': company_obj,
            "has_company":has_company
        }
        return render(request, 'company/add_current_user.html', context)



# Helper function to get all the users
def get_users(company_obj):
    admins = User.objects.filter(company=company_obj, company_role="admin")
    pending_admins = User.objects.filter(company=company_obj, company_role="admin_pending_approval")
    members = User.objects.filter(company=company_obj, company_role="member")
    return {"admins": admins, "pending_admins": pending_admins, "members": members}


# Helper function to get a pretty string of main members
def get_users_string(company_obj):
    users = get_users(company_obj)
    admins = users['admins']
    members = users['members']

    result = ""
    if len(admins) == 0:
        result += "No admin"
    elif len(admins) <= 2:
        result += "Admins: "
        for user in admins:
            result += user.username + ", "
        result = result[:-2]
    else:
        result += "Admins: " + admins[0].username + ", " + admins[1].username \
                  + " and " + str(len(admins)-2) + " other(s) "

    result += ". "


    if len(members) == 0:
        result += "No member"
    elif len(members) <= 2:
        result += "Members: "
        for user in members:
            result += user.username + ", "
        result = result[:-2]
    else:
        result += "Members: " + members[0].username + ", " + members[1].username \
                  + " and " + str(len(members)-2) + " other(s) "


        # result += members[0].username + ", " + members[1].username + " and " + str(len(members)-2) + " other(s) "

    return result
