from django.urls import path
from .views import create_database, create_database_form

urlpatterns = [
    path('create/database/', create_database_form, name='create_database_form'),
    path('api/create/database/', create_database, name='create_database'),
]

