from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from embed_video.fields import EmbedVideoField
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy
from ckeditor_uploader.fields import RichTextUploadingField

from MoCerts.settings import HOST


class CustomUser(AbstractUser):
    ''''расширение модели пользователя'''
    photo = models.ImageField(
        upload_to='accounts/image/%Y/%m/%d', blank=True, verbose_name='Аватарка')
    certificate = models.ForeignKey(
        'Certificate', on_delete=models.SET_NULL, null=True, blank=True)
    telegram_id = models.BigIntegerField(
        verbose_name='telegram id', blank=True, default=0)
    balance = models.PositiveIntegerField(verbose_name='balance', default=0)
    real_account = models.BooleanField(default=True)

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
    number = models.BigIntegerField(verbose_name='Номер сертификата')
    url = models.URLField(max_length=255, verbose_name='Ссылка на сертификат')
    nominal = models.IntegerField(verbose_name='Номинал', default=1)
    user1 = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='first_users')
    user2 = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='second_users')
    user3 = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='third_users')
    published_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    certificate_image = models.ImageField(
        upload_to='certificates/image/%Y/%m/%d', blank=True, verbose_name='Рисунок')
    made_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                related_name='made_by_user')
    is_paid = models.BooleanField(default=False)
    is_accept = models.BooleanField(default=True)
    is_received = models.BooleanField(default=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                              related_name='owner')
    paid_by_user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, default=None, null=True, blank=True,
                                     related_name='paid_by_user')

    def get_url_for_messengers(self):
        """получить ссылку на объект"""
        return f"{HOST + str(reverse('certificate', kwargs={'number': self.number}))}"

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        '''Строковое отображение'''
        return f'{self.number}'

    def get_absolute_url(self):
        """получить ссылку на объект"""
        return reverse('certificate', kwargs={'number': self.number})


class PreviewSettings(models.Model):
    '''модель настройки превью страниц'''
    type = models.CharField(
        max_length=255, default='website', verbose_name='Тип приложения',)
    site_name = models.CharField(
        max_length=255, default='MoCert', verbose_name='Название сайта',)
    title = models.CharField(
        max_length=255, default='Заработай вместе с нами', verbose_name='Заголовок',)
    description = models.CharField(max_length=255, default='Перейди по ссылке и получи сертификат',
                                   verbose_name='Описание',)
    locale = models.CharField(
        max_length=255, default='ru', verbose_name='Локаль',)
    twitter_creator = models.CharField(
        max_length=255, default='@MonteCarlo', verbose_name='twitter_creator',)
    url = models.URLField(max_length=255, default=HOST, verbose_name='Ссылка на сайт',
                          help_text='Данное поле для всех страниц. Для сертификатов подставляется свой url')
    image = models.URLField(max_length=255, default=HOST + '/media/2607211245970578.png', verbose_name='Ссылка на картинку',
                            help_text='Данное поле для всех страниц. Для сертификатов подставляется своя картинка',)

    class Meta:
        verbose_name = 'Настройки превью'
        verbose_name_plural = 'Настройки превью'

    def __str__(self):
        '''Строковое отображени'''
        return f'{self.site_name}'


class ManualPosts(models.Model):
    index_number = models.PositiveIntegerField(
        verbose_name='порядковый номер на странице',)
    title = models.CharField(max_length=255, verbose_name='Заголовок',)
    video = EmbedVideoField(blank=True, verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = 'Инструкцию'
        verbose_name_plural = 'Инструкции'

    def __str__(self):
        '''Строковое отображение'''
        return f'{self.title}'

    def get_absolute_url(self):
        """получить ссылку на объект"""
        return reverse('manual',)


class MainPagePost(models.Model):
    headline = models.CharField(max_length=36, null=False, verbose_name=pgettext_lazy('Заголовок', 'Заголовок'),
                            help_text='максимум 36 символов')
    subtitle = models.CharField(max_length=131, null=False,
                                verbose_name=pgettext_lazy('Подзаголовок', 'Подзаголовок'))
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=pgettext_lazy(
        'Дата публикации', 'Дата публикации'))
    content =  RichTextUploadingField(blank=True, null=True, verbose_name=pgettext_lazy('Содержание', 'Содержание'))

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        '''Строковое отображение'''
        return f'{self.headline}'

    def get_absolute_url(self):
        """получить ссылку на объект"""
        return reverse('postdetail', kwargs={'pk': self.id})