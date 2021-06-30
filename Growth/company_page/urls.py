from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('add', views.add_company_view, name='add_company'),
    path('<int:company_id>/modify', views.modify_company_view, name='modify_company'),
    path('<int:company_id>/', views.my_company_view, name='my_company'),
    path('redirecting', views.redirect_company, name='redirect_company'),
    path('', views.companies_view, name='companies'),
    path('<int:company_id>/delete', views.delete_company_view, name='delete_company'),
    path('<int:company_id>/manage_user', views.manage_users_view, name='manage_users'),
    path('<int:company_id>/add_current_user', views.add_current_user_view, name='add_current_user'),

]

