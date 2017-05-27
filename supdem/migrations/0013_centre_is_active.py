# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0012_auto_20151224_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='centre',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
