# Generated by Django 3.2.5 on 2021-08-03 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_alter_deposit_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawal',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'В процессе'), (2, 'Исполнено'), (3, 'Отклонено')], default=1),
        ),
    ]
