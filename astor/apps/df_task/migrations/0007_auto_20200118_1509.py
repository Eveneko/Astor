# Generated by Django 3.0.2 on 2020-01-18 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_task', '0006_auto_20200118_1508'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='cfg_file',
            new_name='config',
        ),
    ]
