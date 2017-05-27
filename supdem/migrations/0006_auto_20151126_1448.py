# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0005_emaillog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='hash_slug',
        ),
        migrations.AddField(
            model_name='photo',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image', default=0),
            preserve_default=False,
        ),
    ]
