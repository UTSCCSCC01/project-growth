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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from courses import views

from django.conf.urls import url, include


from users import views
from company_page import views as company_page
from courses import views as courses

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # don't forget import include
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    path('forum/', include('forum.urls')),
    url(r'^courses/', include('courses.urls')),

    # Ethan's url
    url(r'^company/add_company', company_page.add_company_view, name='add_company'),
    url(r'^company/modify_company', company_page.modify_company_view, name='modify_company'),
    url(r'^company/', company_page.my_company_view, name='my_company'),
    url(r'^chat/', include('chat.urls')),

    # URL for Courses

    path('', courses.Home.as_view(), name='home'),
    path('upload/', courses.upload, name='upload'),
    path('books/', courses.book_list, name='book_list'),
    path('books/upload/', courses.upload_book, name='upload_book'),
    path('books/<int:pk>/', courses.delete_book, name='delete_book'),

    path('class/books/', courses.BookListView.as_view(), name='class_book_list'),
    path('class/books/upload/', courses.UploadBookView.as_view(), name='class_upload_book'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
