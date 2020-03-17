from django.urls import path

from .views import upload_database

urlpatterns = [
    path('loader/', upload_database, name='loader'),
]
