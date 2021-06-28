from django.shortcuts import render, redirect

from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def register(request):

    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('/')
    else:

        form = RegisterForm()

    return render(request, 'users/register.html', context={'form': form, 'next': redirect_to})


def index(request):
    return render(request, 'index.html')


@login_required
def profile(request, slug):
    # return HttpResponse(slug)
    data = get_user_model().objects.filter(
        username=slug).first()
    return render(request, 'profile/user_profile.html', context={'data': data})
