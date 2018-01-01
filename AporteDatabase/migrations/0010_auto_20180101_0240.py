# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-01 02:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AporteDatabase', '0009_auto_20171231_2311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historialpagos',
            options={'verbose_name': 'Entrada', 'verbose_name_plural': 'Historial de pagos (No Modificar)'},
        ),
        migrations.AlterModelOptions(
            name='identidad',
            options={'verbose_name': 'Identidad del Nodo', 'verbose_name_plural': 'Identidades'},
        ),
        migrations.RemoveField(
            model_name='aportemes',
            name='aporte',
        ),
    ]
