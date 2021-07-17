from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied

from users.models import User
from .models import Company, Photo, File

from .forms import AddCompanyForm, ModifyCompanyForm, AddPhotoForm, AddFileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import os


# Display current user company and company list page
# Public. But users without a company will be prompt to create/join one
def companies_view(request):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        company_obj = None
    else:
        # Get current user's company
        company_obj = request.user.company
    member_list = get_users_string(company_obj) #Get "members: xxx, xxx" string

    # Get all companies
    companies = Company.objects.all()
    # Get "members: xxx, xxx" string and map it into a dictionary
    companies_dict = {company_obj: get_users_string(company_obj) for company_obj in companies }
    # Company photos, sorted from latest to earliest
    photos = Photo.objects.all().order_by('-last_modified')
    # True if current viewer is company admin
    admins = get_users(company_obj)["admins"]
    viewer_is_admin = request.user in admins

    # If current viewer has company, remove their company from company list
    if has_company(request.user):
        companies_dict.pop(company_obj)

    # Show admin pending member requests
    show_new_member_request_for_admin(request, company_obj)

    # When Leave this company button is pressed
    if "leave_this_company" in request.POST:

        #  Additional step, check if there's more admin left
        if viewer_is_admin and len(admins) < 2:  # If it is not the last admin
            # Don't do anything and raise this error message
            messages.error(request, "Cannot remove the last admin! "
                                    "You need to assign at least one other admin or delete the company entirely!")

        else:
            # Remove existing admin/member from company
            user_to_remove = request.user  # User obj of user member to be removed

            user_to_remove.company_role = "member"  # Set role back to member
            user_to_remove.save()

            company_obj.user_set.remove(user_to_remove)  # Remove this user in User model's foreign key column
            return redirect('companies')


    context = {
        "companies_dict": companies_dict, # ALl companies
        "company_obj": company_obj, # Current user's company
        "member_list": member_list, # Current user's company's members
        "photos": photos,
        "has_company":has_company(request.user),
        "is_admin":viewer_is_admin
    }
    return render(request, "company/companies.html", context)

# Page for viewing a company
# Public. But Guest, Member and Admin will see different interactions
def company_profile_view(request, company_id):

    # Get company obj
    company_obj = get_object_or_404(Company, id=company_id)
    # Get users list
    admins, members = get_users(company_obj)["admins"], get_users(company_obj)["members"]

    # True if current viewer is company member
    viewer_is_admin = request.user in admins
    viewer_is_member = request.user in members

    # Company photos,files, sorted from latest to earliest
    photos = company_obj.photo_set.all().order_by('-last_modified')
    files = company_obj.file_set.all().order_by('-last_modified')

    if viewer_is_admin:
        # Show admin pending member requests
        show_new_member_request_for_admin(request, company_obj)

        messages.warning(request,
                         "You are viewing this page as an ADMIN, you have full access to all the page management actions.")


    elif viewer_is_member:
        messages.warning(request,
                         "You are viewing this page as a MEMBER, you have limited access to the page management actions. "
                         "If you need more access including editing company profile, "
                         "membership management, please contact your admin.")

    else:

        messages.info(request,
                         "You are viewing as a GUEST, you cannot edit anything on this page."
                         "If you need more access, please ",
                         extra_tags="guest_view_company_profile")

    # When Leave this company button is pressed
    if "leave_this_company" in request.POST:

        #  Additional step, check if there's more admin left
        if viewer_is_admin and len(admins) < 2:  # If it is not the last admin
            # Don't do anything and raise this error message
            messages.error(request, "Cannot remove the last admin! "
                                    "You need to assign at least one other admin or delete the company entirely!")

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
        "files": files,
        "photos": photos
    }
    return render(request, "company/company_profile.html", context)

# Page for adding a new company
# Public. But only users who are company-less can submit the form
@login_required()
def add_company_view(request):

    # Initiate Django form
    form = AddCompanyForm()
    if request.method == "POST":

        # Check if viewer is already a member of other company
        if has_company(request.user):
            # Return alert message
            messages.error(request, "You already have a company!")
        # Otherwise, generate form
        else:
            form = AddCompanyForm(request.POST or None, request.FILES)

    # Check if the form is valid, if so, get the new object id and save it
    if form.is_valid():

        request.user.company_role = "admin"  # Set role back to admin by default
        request.user.save()

        new_company = form.save() # Get django generated obj from form completion
        new_company.user_set.add(request.user) # Add current user to company

        # When success, go back to company page while passing the new id
        return redirect('manage_users' , company_id=new_company.id)


    # If the form is not valid, re-run the form
    context = {
        'form' : form
    }
    return render(request, "company/add_company.html", context)

# Page for company owners to edit their company
# Admins only. 403 otherwise
@login_required()
def modify_company_view(request, company_id):

    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # If user does not have right level of access
    check_has_enough_access(request,company_obj,"admin")

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

# Page for company owners to confirm deletion of the company
# Admins only. 403 otherwise
@login_required()
def delete_company_view(request, company_id):
    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # If user does not have right level of access
    check_has_enough_access(request,company_obj,"admin")

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
# Admins only. 403 otherwise
@login_required()
def manage_users_view(request, company_id):

    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # If user does not have right level of access
    check_has_enough_access(request,company_obj,"admin")

    # Users that do not have a company yet and is available
    users_available = User.objects.filter(company=None)
    # Current members in the company
    admins, members, pending_members = get_users(company_obj)["admins"], get_users(company_obj)["members"], \
                                       get_users(company_obj)["pending_members"]

    # When posting the form
    if request.method == "POST":

        # When "Approve" Button is pressed on manage member page
        if "add_new_member" in request.POST:

            # Add new member to company
            userId = request.POST.get('user_to_add') # UserId of user member to be added
            user = User.objects.get(id=userId) # User obj of user member to be added

            user.company_role = "member"  # Set role to member from pending_member
            user.save()

            company_obj.user_set.add(user) # Add this user in User model's foreign key column
            messages.success(request,"User {0} was successfully added to your company! ".format(user.username))

        # When "Reject" Button is pressed on manage member page
        elif "reject_new_member" in request.POST:

            # Add new member to company
            userId = request.POST.get('user_to_add') # UserId of user member to be added
            user = User.objects.get(id=userId) # User obj of user member to be added

            user.company_role = "member"  # Set role to member from pending_member
            user.company = None # Clear user's reuqest company status
            user.save()

            messages.warning(request,"User {0}'s request was rejected".format(user.username))

        # When "Add" Button is pressed on manage member page
        elif "add_user" in request.POST:

            # Add new user to company
            userId = request.POST.get('user_to_add') # UserId of user member to be added
            user = User.objects.get(id=userId) # User obj of user member to be added

            user.company_role = "member"  # Set role to member
            user.save()

            company_obj.user_set.add(user) # Add this user in User model's foreign key column
            messages.success(request,"User {0} was successfully added to your company! ".format(user.username))

        # When Remove (admin) button is pressed
        elif "remove_admin" in request.POST:

            if len(admins) >= 2: # If it is not the last admin

                # Remove existing admin from company
                userId = request.POST.get('user_to_remove') # UserId of user member to be removed
                user = User.objects.get(id=userId) # User obj of user member to be removed

                user.company_role = "member" # Set role back to member
                user.save()

                company_obj.user_set.remove(user)  # Remove this user in User model's foreign key column

                messages.success(request,
                                 "Admin {0} was successfully removed from your company! "
                                 .format(user.username))
            else:
                # Don't do anything and raise this error message
                messages.error(request, "Cannot remove the last admin! "
                                        "You need to assign at least one other admin or delete the company entirely!")

        # When Remove (member) button is pressed
        elif "remove_member" in request.POST:

            # Remove existing users form company
            userId = request.POST.get('user_to_remove') # UserId of user member to be removed
            user = User.objects.get(id=userId) # User obj of user member to be removed

            user.company_role = "member"
            user.save()
            company_obj.user_set.remove(user)  # Remove this user in User model's foreign key column

            messages.success(request,
                             "Member {0} was successfully removed from your company! "
                             .format(user.username))

        # When set_as_member (admin) button is pressed
        elif "set_as_member" in request.POST:

            # Additional step, check if there's more admin left
            if len(admins) >= 2: # If it is not the last admin

                # Get the admin object
                userId = request.POST.get('user_to_remove') # UserId of user member to be removed
                user = User.objects.get(id=userId) # User obj of user member to be removed

                user.company_role = "member" # Set role back to member
                user.save()

                messages.success(request, "Admin {0} was successfully set as a member! ".format(user.username))

            else:
                # Don't do anything and raise this error message
                messages.error(request, "Cannot set the last admin to member!")

        # When set_as_admin (member) button is pressed
        elif "set_as_admin" in request.POST:

            userId = request.POST.get('user_to_remove')  # UserId of user member to be removed
            user = User.objects.get(id=userId)  # User obj of user member to be removed

            user.company_role = "admin"  # Set role back to member
            user.save()

            messages.success(request, "Member {0} was successfully set as a admin! ".format(user.username))

        # On success, go back to company profile page
        return redirect('manage_users' , company_id=company_id)

    # When just viewing the form
    else:

        context = {
            'users_available': users_available,
            'company_obj': company_obj,
            'admins': admins,
            'members': members,
            'pending_members': pending_members
        }
        return render(request, 'company/manage_users.html', context)

# Page for company members to manage company photos
# Member or Admin only. 403 otherwise
@login_required()
def manage_photos_view(request, company_id):
    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # If user does not have right level of access
    check_has_enough_access(request,company_obj,"member")

    # Company photos, sorted from latest to earliest
    photos = company_obj.photo_set.all().order_by('-last_modified')

    INITIAL_DATA = {'company': company_obj}

    # Initiate Django form and pass company obj in
    form = AddPhotoForm(initial=INITIAL_DATA)

    if request.method == "POST":

        # When "Upload" Button is pressed on manage member page
        if "add_photo" in request.POST:

            # **** Need to pass initial company object, otherwise new Photo obj will raise lack attribute error
            form = AddPhotoForm(request.POST or None, request.FILES, initial=INITIAL_DATA)

            # Check if the form is valid, if so, get the new object id and save it
            if form.is_valid():

                new_photo = form.save() # Get django generated obj from form completion
                company_obj.photo_set.add(new_photo) # Add new photo to company

                messages.success(request, "Photo successfully added!")

        # When "Remove" Button is pressed on manage member page
        elif "remove_photo" in request.POST:

            # Remove existing users form company
            photoId = request.POST.get('photo_to_remove') # UserId of user member to be removed
            photo_to_remove = Photo.objects.get(id=photoId) # User obj of user member to be removed
            old_photo_path = photo_to_remove.photo.path

            # Remove the old photo object from db
            photo_to_remove.delete()

            # Remove old uploaded logo image.
            os.remove(old_photo_path)

            messages.success(request, "Photo successfully removed!")

        # When success, go back to company page while passing the new id
        return redirect('manage_photos', company_id=company_id)

    # If the form is not valid, or just viewing, re-run the form
    context = {
        "company_obj": company_obj,
        'form': form,
        'photos': photos,
    }
    return render(request, "company/manage_photos.html", context)

# Page for company members to manage company files
# Member or Admin only. 403 otherwise
@login_required()
def manage_files_view(request, company_id):
    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    # If user does not have right level of access
    check_has_enough_access(request,company_obj,"member")

    # Company photos, sorted from latest to earliest
    files = company_obj.file_set.all().order_by('-last_modified')

    INITIAL_DATA = {'company': company_obj}

    # Initiate Django form and pass company obj in
    form = AddFileForm(initial=INITIAL_DATA)

    if request.method == "POST":

        # When "Upload" Button is pressed on manage member page
        if "add_file" in request.POST:

            # **** Need to pass initial company object, otherwise new Photo obj will raise lack attribute error
            form = AddFileForm(request.POST or None, request.FILES, initial=INITIAL_DATA)

            # Check if the form is valid, if so, get the new object id and save it
            if form.is_valid():

                new_file = form.save() # Get django generated obj from form completion
                company_obj.file_set.add(new_file) # Add new photo to company

                messages.success(request, "File successfully added!")

        # When "Remove" Button is pressed on manage member page
        elif "remove_file" in request.POST:

            # Remove existing users form company
            fileId = request.POST.get('file_to_remove') # UserId of user member to be removed
            file_to_remove = File.objects.get(id=fileId) # User obj of user member to be removed
            old_path = file_to_remove.file.path

            # Remove the old photo object from db
            file_to_remove.delete()

            # Remove old uploaded logo image.
            os.remove(old_path)

            messages.success(request, "File successfully removed!")

        # When success, go back to company page while passing the new id
        return redirect('manage_files', company_id=company_id)

    # If the form is not valid, or just viewing, re-run the form
    context = {
        "company_obj": company_obj,
        'form': form,
        'files': files,
    }
    return render(request, "company/manage_files.html", context)

# Page for users to join a company
# Public except users not logged in, But only users who are company-less can submit form
@login_required()
def join_company_view(request, company_id):

    # Get the company object
    company_obj = get_object_or_404(Company, id = company_id)

    if has_company(request.user):
        messages.error(request,"Cannot join this company because you have already joined another company.")

    # When posting the form
    if request.method == "POST":

        if "user_request_to_be_member" in request.POST:

            # Set the new_user's company_role as pending_member
            # Company admin can see list of pending members and approve them
            new_user = request.user

            new_user.company_role = "pending_member"  # Set role to pending_member
            new_user.save()

            company_obj.user_set.add(new_user)

            messages.success(request, "Request sent to admin!")


        if "user_request_to_be_admin" in request.POST:

            # Add new user to company and set to admin
            new_user = request.user

            new_user.company_role = "admin"  # Set role back to member
            new_user.save()

            company_obj.user_set.add(new_user)

        return redirect('company_profile' , company_id=company_id)

    # When just viewing the form
    else:

        # True if this company has a working admin
        has_admin = len(get_users(company_obj)['admins']) > 0

        context = {
            'company_obj': company_obj,
            "has_company":has_company(request.user),
            'has_admin': has_admin
        }
        return render(request, 'company/join_company.html', context)

'''
Our great and helpful helpers are as below

'''

# Returns True if user has a company
def has_company(user):
    # True if user has a company
    # TODO: Check for user role (Partner, instructor will pass)
    if user.is_authenticated and user.role == "Student":
        return (user.company != None) and (user.company_role != "pending_member") # user is not an unapproved member
    else: return False

# Helper function to get all the users
def get_users(company_obj):
    admins = User.objects.filter(company=company_obj, company_role="admin")
    pending_members = User.objects.filter(company=company_obj, company_role="pending_member")
    members = User.objects.filter(company=company_obj, company_role="member")
    return {"admins": admins, "pending_members": pending_members, "members": members}

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
    return result

# Helper function to see if user has minimal level of role required access to see this page
# Param: request, company_obj, required_role = "admin" or "member"
# Raise 403 forbidden if minimal required role is not reached
def check_has_enough_access(request, company_obj, required_role):
    is_admin = request.user in get_users(company_obj)["admins"]
    is_member = request.user in get_users(company_obj)["members"]
    if required_role == "admin":
        if not is_admin:
            messages.error(request, "Only ADMINS of this company can see this page")
            raise PermissionDenied()
    elif required_role == "member": # Can be member or admin
        if not (is_admin or is_member):
            messages.error(request, "Only MEMBERS of this company can see this page")
            raise PermissionDenied()

# Input: Request, Company company
# This function will check if current user is admin,
# And show the user pending requests if so.
def show_new_member_request_for_admin(request, company_obj):
    # True if current viewer is company member
    is_admin = request.user in get_users(company_obj)["admins"]
    # IF user is admin and there are pending member request
    if is_admin and company_obj:
        # Get pending members
        pending_members = company_obj.user_set.filter(company_role="pending_member")
        for user in pending_members:
            messages.success(request,
                          "There is a pending member request: {0}".format(user.username),
                          extra_tags='new_member_request')
