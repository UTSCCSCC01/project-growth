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

from courses import views as course_views

from django.conf.urls import url, include
import notifications.urls
import notificationsForum.urls



from users import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # don't forget import include
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    path('forum/', include('forum.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^calendar/', include('cal.urls'), name='calendar'),
    path(r'home', views.app_home, name='home'),

    path(r'dashboard', views.dashboard, name='dashboard'),

    path(r'profile/<slug:slug>/', views.profile, name='profile'),
    path('edit_profile/<slug:slug>/', views.edit_profile, name='edit_profile'),
    path('search_profile/',
         views.search_profile, name='search_profile'),
    path('company/', include('company_page.urls')),
    url(r'^chat/', include('chat.urls')),
    url(r'^video_chat/', include('video_chat.urls')),
    url(r'^direct/', include('direct.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url('^inbox/notificationsForum/', include(notificationsForum.urls, namespace='notificationsForum')),

    path('', course_views.Home.as_view(), name='home'),
    path('upload/', course_views.upload, name='upload'),
    path('books/', course_views.book_list, name='book_list'),

    path('books/upload_l/', course_views.upload_list, name='upload_list'),

    path('books/upload/', course_views.upload_book, name='upload_book'),
    
    path('books/upload_l/uploadm/', course_views.upload_upload, name='upload_upload'), 


    path('books/<int:pk>/', course_views.delete_book, name='delete_book'),

    path('books/upload_l/<int:pk>/', course_views.delete_upload, name='delete_upload'), 

    # Upload Mark
    
    path('books/upload_l/uploadmark/', course_views.upload_mark, name='upload_mark'), 

    # Result
    
    path('books/upload_l/uploadresult/', course_views.result, name='result'),  

    # Class Method

    path('class/books/', course_views.BookListView.as_view(), name='class_book_list'),
    path('class/books/upload/', course_views.UploadBookView.as_view(),
         name='class_upload_book'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
