# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0013_centre_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialogue',
            name='creationdate',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 19, 33, 15, 747299, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='creationdate',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 23, 19, 33, 22, 663414, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
