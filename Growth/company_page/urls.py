from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('add_company', views.add_company_view, name='add_company'),
    path('<int:company_id>/modify_company', views.modify_company_view, name='modify_company'),
    path('<int:company_id>/', views.my_company_view, name='my_company'),
    path('redirecting', views.redirect_company, name='redirect_company'),
    path('no_company', views.no_company_view, name='no_company'),

]

