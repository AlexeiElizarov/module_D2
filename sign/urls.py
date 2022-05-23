from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *


urlpatterns = [
    path('login/',
         LoginView.as_view(template_name = 'sign/login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name = 'sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name = 'sign/signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me,
         name = 'upgrade'),
    path('user_profile/', ShowProfilePageView.as_view(),
         name='user_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(),
         name='create_user_profile'),
    path('edit_profile_page/', UpdateProfilePageView.as_view(),
         name='edit_user_profile')
]