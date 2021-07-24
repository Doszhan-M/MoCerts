# Generated by Django 3.2.5 on 2021-07-23 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0006_auto_20210722_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='status',
        ),
        migrations.AddField(
            model_name='certificate',
            name='accept_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='certificate',
            name='payment_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='balance',
            field=models.PositiveIntegerField(default=0, verbose_name='balance'),
        ),
    ]