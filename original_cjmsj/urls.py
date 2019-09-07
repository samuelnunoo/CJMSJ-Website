"""DjangoWebSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from blogs.views import main_page,contact,about
from users.views import team, update_profile
from django.contrib.auth import views
from users.forms import LoginForm
from blogs.views import submit, authorized
from submissions.views import ProfileAutocomplete
from django.contrib.auth import views as auth_views



urlpatterns = [


    path('admin-cjmsj/', admin.site.urls),
    path('users/', include('users.urls')),
    path('blogs/', include('blogs.urls')),
    path('',main_page,name='home' ),
    path('team/', team, name='team'),

    #Log-In Log-Out
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view()),

    #S
    path('contact/',contact,name='about'),
    path('about/',about,name='contact'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ajax/submit', submit, name='submit'),
    path('ajax/authorized',authorized, name='authorized'),
    path('profile-autocomplete', ProfileAutocomplete.as_view(),name='profile-autocomplete'),
    path('ajax/profile',update_profile, name='update_profile'),

    # Password Reset
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='account/forgot_password.html'), name ='password_reset'),
    #path('password_reset/',auth_views.PasswordResetConfirmView.as_view(template_name='account/email_sent.html'), name = 'password_reset_confirm'),
    path('password_reset/done',auth_views.PasswordResetDoneView.as_view(template_name='account/email_sent.html'), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/new_password.html'), name = 'password_reset_confirm'),
    path('password_reset/complete',auth_views.PasswordResetCompleteView.as_view(template_name='account/reset_done.html'), name ='password_reset_complete'),



    ]
