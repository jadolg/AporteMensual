# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-10-23 02:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('AporteDatabase', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialgastos',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 10, 23, 2, 46, 28, 311000, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
