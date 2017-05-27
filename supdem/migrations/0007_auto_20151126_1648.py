# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0006_auto_20151126_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.CharField(max_length=200),
        ),
    ]
