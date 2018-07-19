from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('search_organisms/', views.search_organisms, name="Search Organisms"),
    path('search_artifacts/', views.search_artifacts, name="Search Artifacts"),
    path('search_fossils/', views.search_fossils, name="Search Fossils"),
    path('search_artworks/', views.search_artworks, name="Search Artworks"),
    path('', views.index, name='index')
]