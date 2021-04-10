# custom urls file in order keep the overall organization of the project

from django.urls import path

from . import views

urlpatterns = [
    # route for the home page
    path('', views.index, name="index"),    
]