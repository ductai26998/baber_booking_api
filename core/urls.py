"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from account.views import (SalonLoginWithEmailOrUsername, SalonRegister,
                           SalonVerifyOTP, UserLoginWithEmailOrUsername,
                           UserRegister, UserVerifyOTP)
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    url(r"account/", include('account.urls')),
    url('register-user', UserRegister.as_view(), name='register-user'),
    url('verify-user', UserVerifyOTP.as_view(), name='verify-user'),
    url('register-salon', SalonRegister.as_view(), name='register-salon'),
    url('verify-salon', SalonVerifyOTP.as_view(), name='verify-salon'),
    url('login-user', UserLoginWithEmailOrUsername.as_view(), name='login-user'),
    url('login-salon', SalonLoginWithEmailOrUsername.as_view(), name='login-salon'),
]
