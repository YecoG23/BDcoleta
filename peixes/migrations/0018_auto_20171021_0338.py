# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-21 05:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peixes', '0017_auto_20170822_1522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lote',
            options={'permissions': (('can_edit', 'Can edit a lote of peixes'), ('can_delete', 'Can delete a lote of peixes'), ('can_view', 'Can edit a lote of peixes')), 'verbose_name_plural': 'Lotes'},
        ),
    ]
