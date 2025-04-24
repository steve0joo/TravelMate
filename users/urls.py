from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('reset/', views.reset_user_view, name='reset_user'),
    path('spotlight/', views.spotlight_view, name='spotlight'),
]