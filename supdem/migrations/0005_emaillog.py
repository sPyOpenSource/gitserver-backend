# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('supdem', '0004_myuser_languagecode'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
                ('email_name', models.CharField(max_length=50)),
                ('status', models.PositiveSmallIntegerField()),
                ('to_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
