# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-23 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AporteDatabase', '0005_auto_20161024_0101'),
    ]

    operations = [
        migrations.AddField(
            model_name='aportemes',
            name='comentarios',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='historialpagos',
            name='comentarios',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
