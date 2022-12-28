"""Module providingFunction printing python version."""
from django.urls import path
from files.views import *

from files import views

urlpatterns = [
    path("track/", views.TrackFileView, name="track"),
    path("update-file/<str:slug>", views.OwnFileHistory, name="history"),
    path("history/<str:slug>", views.GetFileHistory, name="history"),
    path('',views.home,name="home"), 
    path('about/',views.about,name="about"),
    path('contact',views.contact,name="contact"), 
    path('signup',views.handleSignup,name="handleSignup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handlelogout,name="handlelogout"),
    path("create-file/", views.CreateFileView, name="createfile"),
    path("files/", views.GetAllFiles, name="allfiles"),
    path("files/<str:slug>", views.GetFile, name="getfile"),
]