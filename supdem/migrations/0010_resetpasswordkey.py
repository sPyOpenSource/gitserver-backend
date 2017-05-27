# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0009_auto_20151126_1840'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPasswordKey',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('key', models.CharField(unique=True, max_length=200)),
                ('expirydate', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
