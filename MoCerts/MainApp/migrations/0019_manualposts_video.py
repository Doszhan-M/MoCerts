# Generated by Django 3.2.5 on 2021-07-27 06:43

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0018_auto_20210727_0637'),
    ]

    operations = [
        migrations.AddField(
            model_name='manualposts',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, verbose_name='Видео'),
        ),
    ]