# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-25 01:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('peixes', '0010_auto_20170724_2218'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projeto',
            options={'ordering': ['-nome'], 'permissions': (('can_check_projeto', 'Can check any project'),), 'verbose_name_plural': 'Projetos'},
        ),
    ]
