# Generated by Django 3.2.5 on 2021-07-22 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_auto_20210721_1259'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='balance',
            field=models.IntegerField(default=0, verbose_name='balance'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='telegram_id',
            field=models.BigIntegerField(blank=True, default=0, verbose_name='telegram id'),
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BigIntegerField(verbose_name='Номер сертификата')),
                ('url', models.URLField(max_length=255, verbose_name='Ссылка на сертификат')),
                ('nominal', models.IntegerField(default=1, verbose_name='Номинал')),
                ('published_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')),
                ('certificate_image', models.ImageField(default=None, upload_to='')),
                ('status', models.CharField(choices=[('NONE', ''), ('RECEIVED', 'Получен'), ('PAID', 'Оплачен')], default='NONE', max_length=15)),
                ('made_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='made_by_user', to=settings.AUTH_USER_MODEL)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='first_users', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='second_users', to=settings.AUTH_USER_MODEL)),
                ('user3', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='third_users', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сертификат',
                'verbose_name_plural': 'Сертификаты',
            },
        ),
        migrations.AddField(
            model_name='customuser',
            name='certificate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='MainApp.certificate'),
        ),
    ]
