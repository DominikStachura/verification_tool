from django.urls import path
from . import views


app_name = 'front'

urlpatterns = [
    path('', views.index, name="index"),
    path('update', views.update, name="update"),
    path('index.html', views.index, name="index"),
    path('validator.html', views.validator, name="validator"),
    path('tables.html', views.tables, name="tables")

]
