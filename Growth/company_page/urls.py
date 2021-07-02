from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('add', views.add_company_view, name='add_company'),
    path('<int:company_id>/modify', views.modify_company_view, name='modify_company'),
    path('<int:company_id>/', views.company_profile_view, name='company_profile'),
    path('', views.companies_view, name='companies'),
    path('<int:company_id>/delete', views.delete_company_view, name='delete_company'),
    path('<int:company_id>/manage_users', views.manage_users_view, name='manage_users'),
    path('<int:company_id>/manage_photos', views.manage_photos_view, name='manage_photos'),
    path('<int:company_id>/manage_files', views.manage_files_view, name='manage_files'),
    path('<int:company_id>/join_company', views.join_company_view, name='join_company'),

]

