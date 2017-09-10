# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 14:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0024_myuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=5),
        ),
    ]
