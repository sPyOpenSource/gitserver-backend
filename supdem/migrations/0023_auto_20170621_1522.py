# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-21 15:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0022_auto_20170621_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='Owner',
            new_name='owner',
        ),
    ]
