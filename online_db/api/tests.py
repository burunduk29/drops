from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Database


class UserTests(TestCase):
    def test_user_registration(self):
        # Проверка процесса регистрации пользователя
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword15',
            'password2': 'testpassword15',
        })
        self.assertEqual(response.status_code, 302)  # проверка перенаправления после успешной регистрации
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

    def test_login(self):
        # Проверка входа в систему
        user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword15',
        })
        self.assertEqual(response.status_code, 302)  # проверка перенаправления после успешного входа


class DatabaseTests(TestCase):
    def test_create_database(self):
        # Тест создания базы данных
        user = get_user_model().objects.create_user(username='testuser', password='testpassword15')
        self.client.login(username='testuser', password='testpassword15')

        response = self.client.post(reverse('create_database'), {
            'name': 'my_database',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Database.objects.filter(name='my_database').exists())
