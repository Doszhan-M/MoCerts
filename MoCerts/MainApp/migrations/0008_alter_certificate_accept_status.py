# Generated by Django 3.2.5 on 2021-07-23 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0007_auto_20210723_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='accept_status',
            field=models.BooleanField(),
        ),
    ]