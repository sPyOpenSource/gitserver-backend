# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='active_dialogue',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
