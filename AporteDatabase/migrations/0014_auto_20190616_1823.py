# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-16 22:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AporteDatabase', '0013_auto_20190616_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='usuario',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
