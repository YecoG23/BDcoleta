# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-30 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peixes', '0024_auto_20171125_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tecido',
            name='data',
            field=models.DateField(blank=True, null=True),
        ),
    ]
