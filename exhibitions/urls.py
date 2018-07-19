from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('search_artifacts/', views.search_artifacts, name="Search Artifacts"),
    path('', views.index, name='index')
]