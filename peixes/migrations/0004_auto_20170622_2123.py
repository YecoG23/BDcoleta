# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-23 00:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peixes', '0003_auto_20170618_1424'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projeto',
            old_name='autorização',
            new_name='curador',
        ),
    ]
