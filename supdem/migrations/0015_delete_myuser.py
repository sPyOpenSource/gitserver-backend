# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-27 14:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0014_auto_20160123_2033'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]