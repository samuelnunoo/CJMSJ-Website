from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from users import views as core_views


#Importing this so that I can connect to default views


app_name='users'
urlpatterns = [
    path('signup/account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',core_views.activate, name='activate'),
    path('signup/',core_views.signup,name='signup'),
    path('invalid/',core_views.invalid,name='invalid'),
    path('<int:id>',core_views.profile,name='pages'),
    path('profile/',core_views.user_profile,name='user_profile')

    # The 3rd parameter allows me to pass custom form content

  #  path('profile/',name='page')
]
