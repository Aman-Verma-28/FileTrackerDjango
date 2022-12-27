"""Module providingFunction printing python version."""
from django.urls import path
from files.views import *

from files import views

urlpatterns = [
    # path("register/", RegisterView.as_view(), name="register"),
    # path("login/", LoginView.as_view(), name="login"),
    # path('about/', AboutView.as_view(),name="about"),
    # path('', HomeView.as_view(),name="home"),
    # path("profile/", ProfileView.as_view(), name="profile"),
    # path("contact/", ContactView.as_view(), name="contact"),
    # path("logout/", LogoutView.as_view(), name="logout"),
    # path('search',views.search,name="search"),
    
    #  path('video_feed', views.video_feed, name='video_feed'),
# ]

# urlpatterns = [
    path("track/", views.TrackFileView, name="track"),
    path("update-file/<str:slug>", views.OwnFileHistory, name="history"),
    path("history/<str:slug>", views.GetFileHistory, name="history"),
    path('',views.home,name="home"), 
    path('about/<str:authSlug>',views.about,name="about"),
    path('contact',views.contact,name="contact"), 
    path('signup',views.handleSignup,name="handleSignup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handlelogout,name="handlelogout"),
    path("create-file/", views.CreateFileView, name="createfile"),
    path("files/", views.GetAllFiles, name="allfiles"),
    path("files/<str:slug>", views.GetFile, name="getfile"),
]