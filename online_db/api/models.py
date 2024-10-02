from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Добавляем related_name для полей groups и user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Изменили related_name для групп
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Изменили related_name для разрешений
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
class Database(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=256, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name