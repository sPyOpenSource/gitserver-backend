# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0007_auto_20151126_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.CharField(max_length=200, default=None, blank=True),
        ),
    ]
