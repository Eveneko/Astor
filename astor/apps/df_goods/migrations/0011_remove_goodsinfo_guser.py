# Generated by Django 3.0.2 on 2020-01-15 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0010_auto_20191226_1325'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodsinfo',
            name='guser',
        ),
    ]
