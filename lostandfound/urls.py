"""lostandfound URL Configuration

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
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from .models import *


urlpatterns = [
    path('',views.first),
    path('index',views.index),
    path('reg',views.reg),
    path('registration',views.registration),
    path('login/',views.login),
    #path('login/addlogin',views.addlogin),
    path('login/addlogin',views.addlogin),
    path('logout/',views.logout),
    path('cat',views.cat),
    path('addcat',views.addcat),
    path('lostt',views.lostt),
    path('found',views.found),
    path('addlostt',views.addlostt),
    path('addfound',views.addfound),
    path('profile',views.profile),
    path("update_myprofile/<int:id>/", views.update_myprofile, name="update_myprofile"),
    path("update_profile/<int:id>/", views.update_profile, name="update_profile"),

    path('viewstudentreq',views.viewstudentreq),

    path('studreqaccept/<int:id>',views.studreqaccept),
    path('studreqreject/<int:id>',views.studreqreject),

    path('viewreq',views.viewreq),
    path('viewfound',views.viewfound),
    path('viewlostmatch',views.view_matches_for_lost),
    path('reqaccept/<int:id>',views.reqaccept),
    path('reqreject/<int:id>',views.reqreject),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

