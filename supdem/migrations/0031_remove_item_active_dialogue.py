# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-24 15:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0030_auto_20170715_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='active_dialogue',
        ),
    ]