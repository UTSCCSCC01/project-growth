"""Growth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from users import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # don't forget import include
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    path('forum/', include('forum.urls')),
    url(r'^courses/', include('courses.urls')),
    path(r'profile/<slug:slug>/', views.profile, name='profile'),
    path('edit_profile/<slug:slug>/', views.edit_profile, name='edit_profile'),
    path('search_profile/',
         views.search_profile, name='search_profile'),
    # Ethan's url
    path('company/', include('company_page.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^direct/', include('direct.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
