from django.urls import path
from . import views

urlpatterns=[
    path('users/',views.users, name="users"),
    path('profiles/', views.profile, name="profiles"),
     path('register/', views.register, name="register"),
]