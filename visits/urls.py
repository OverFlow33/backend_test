# custom urls file in order keep the overall organization of the project

from django.urls import path

from . import views

urlpatterns = [
    # route to the stats web page
    path('stats/', views.stats, name="stats"),
]