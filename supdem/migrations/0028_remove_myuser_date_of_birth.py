# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-25 19:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0027_auto_20170625_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='date_of_birth',
        ),
    ]
