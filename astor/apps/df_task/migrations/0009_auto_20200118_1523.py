# Generated by Django 3.0.2 on 2020-01-18 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_task', '0008_auto_20200118_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='update_time',
            field=models.TimeField(auto_now=True, verbose_name='上次修改时间'),
        ),
    ]
