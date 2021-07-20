from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ''''кастомный юзер'''
    photo = models.ImageField(
        upload_to='accounts/image/%Y/%m/%d', blank=True, verbose_name='Аватарка')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        '''Строковое отображение поста'''
        return f'{self.username}'

    # def get_absolute_url(self):
    #     """получить ссылку на объект"""
    #     return reverse('profile')
