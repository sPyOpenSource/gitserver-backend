# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0011_auto_20151127_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='centre',
            name='show_message_for_locals',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='centre',
            name='show_message_for_refugees',
            field=models.BooleanField(default=False),
        ),
    ]
