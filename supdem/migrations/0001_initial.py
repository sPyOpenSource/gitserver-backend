# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=255, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name_en', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name_en', models.CharField(max_length=100)),
                ('category', models.ForeignKey(to='supdem.Category')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryQuestionOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name_en', models.CharField(max_length=100)),
                ('order', models.PositiveSmallIntegerField()),
                ('categoryquestion', models.ForeignKey(to='supdem.CategoryQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('countrycode', models.CharField(max_length=2)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='DebugLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('last_change', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('is_offer', models.BooleanField()),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
                ('expirydate', models.DateTimeField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('active_dialogue', models.OneToOneField(to='supdem.Dialogue', related_name='+', blank=True)),
                ('category', models.ForeignKey(to='supdem.Category')),
                ('centre', models.ForeignKey(to='supdem.Centre')),
                ('poster', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('creationdate', models.DateTimeField(auto_now_add=True)),
                ('from_poster', models.BooleanField()),
                ('description', models.TextField()),
                ('languagecode', models.CharField(max_length=2)),
                ('dialogue', models.ForeignKey(to='supdem.Dialogue')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('hash_slug', models.SlugField(unique=True)),
                ('item', models.ForeignKey(to='supdem.Item')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('answer', models.ForeignKey(to='supdem.CategoryQuestionOption')),
                ('item', models.ForeignKey(to='supdem.Item')),
            ],
        ),
        migrations.AddField(
            model_name='dialogue',
            name='item',
            field=models.ForeignKey(to='supdem.Item'),
        ),
        migrations.AddField(
            model_name='dialogue',
            name='reactor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
