# Generated by Django 3.2.5 on 2021-07-24 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0013_rename_payment_status_certificate_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='is_received',
            field=models.BooleanField(default=False),
        ),
    ]
