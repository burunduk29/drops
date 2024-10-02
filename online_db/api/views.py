import os
import sqlite3
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm
from .models import Database



def create_database_form(request):
    return render(request, 'create_database.html')

# Создание бдшки
@api_view(['POST'])
def create_database(request):
    db_name = request.data.get('name')
    if not db_name:
        return Response({"error": "Database name is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Проверка существования бд
    db_path = os.path.join(settings.BASE_DIR, f"{db_name}.sqlite3")
    if os.path.exists(db_path):
        return Response({"error": "Database with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

    # Создание бд
    conn = sqlite3.connect(db_path)
    conn.close()

    return Response({"status": "Database created successfully", "db_name": db_name})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('create_database_form')  # перенаправление на страницу создания базы данных
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})




# Пример проверки токена в API для создания таблицы
@api_view(['POST'])
def create_table(request):
    db_name = request.data.get('database')
    token = request.data.get('token')

    # Поиск базы данных по имени
    try:
        database = Database.objects.get(name=db_name)
    except Database.DoesNotExist:
        return Response({"error": "Database not found"}, status=status.HTTP_404_NOT_FOUND)

    # Проверка токена
    if database.token != token:
        return Response({"error": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)

    # Если токен верен, выполняем действия с таблицей (например, создаем таблицу)
    # Ваша логика для создания таблицы
    return Response({"status": "Table created successfully"})
