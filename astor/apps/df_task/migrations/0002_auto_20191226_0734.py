# Generated by Django 2.0.12 on 2019-12-26 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_task', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='cpu',
            field=models.CharField(default='1', max_length=100, verbose_name='cpu'),
        ),
        migrations.AddField(
            model_name='task',
            name='memory',
            field=models.CharField(default='128', max_length=100, verbose_name='mem'),
        ),
    ]
