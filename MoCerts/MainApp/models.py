from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ''''кастомный юзер'''
    photo = models.ImageField(
        upload_to='accounts/image/%Y/%m/%d', blank=True, verbose_name='Аватарка')
    certificate = models.ForeignKey('Certificate', on_delete=models.SET_NULL, null=True, blank=True)
    telegram_id = models.BigIntegerField(verbose_name='telegram id', blank=True, default=0)
    balance = models.IntegerField(verbose_name='balance', default=0)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        '''Строковое отображение'''
        return f'{self.first_name}'

    def get_absolute_url(self):
        """получить ссылку на объект"""
        return reverse('profile')


class Certificate(models.Model):
    '''модель сертификата'''
    STATUS = [
        ('NONE', ''),
        ('RECEIVED', 'Получен'),
        ('PAID', 'Оплачен'),
    ]
    number = models.BigIntegerField(verbose_name='Номер сертификата')
    url = models.URLField(max_length=255, verbose_name='Ссылка на сертификат')
    nominal = models.IntegerField(verbose_name='Номинал', default=1)
    user1 = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='first_users')
    user2 = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='second_users')
    user3 = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='third_users')
    published_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    certificate_image = models.ImageField(default=None)
    made_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                related_name='made_by_user')
    status = models.CharField(max_length=15, choices=STATUS, default='NONE')

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        '''Строковое отображение'''
        return f'{self.number}'

    def get_absolute_url(self):
        """получить ссылку на объект"""
        return reverse('profile')

    