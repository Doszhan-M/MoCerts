# Generated by Django 3.2.5 on 2021-07-28 08:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0024_auto_20210728_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpagepost',
            name='subtitle',
            field=ckeditor.fields.RichTextField(max_length=255, verbose_name='Подзаголовок'),
        ),
    ]
