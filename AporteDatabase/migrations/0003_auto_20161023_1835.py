# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-23 18:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AporteDatabase', '0002_historialgastos_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='aportemes',
            name='cant_usuarios',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='aportemes',
            name='rango',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
