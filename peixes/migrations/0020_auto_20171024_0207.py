# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-24 04:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peixes', '0019_auto_20171021_0340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projeto',
            options={'ordering': ['-nome'], 'permissions': (('can_view_projeto', 'Can check any project'),), 'verbose_name_plural': 'Projetos'},
        ),
    ]
