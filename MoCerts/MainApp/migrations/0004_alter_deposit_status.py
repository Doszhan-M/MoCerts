# Generated by Django 3.2.5 on 2021-08-03 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_auto_20210803_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'В ожидании'), (2, 'Оплачено'), (3, 'Истекший'), (4, 'Отклонено')], default=1),
        ),
    ]
