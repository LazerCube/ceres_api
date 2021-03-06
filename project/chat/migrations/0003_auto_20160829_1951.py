# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-29 18:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20160822_1707'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='name',
        ),
        migrations.AddField(
            model_name='room',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=b'title', verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='room',
            name='title',
            field=models.CharField(default=datetime.datetime(2016, 8, 29, 18, 51, 19, 995000, tzinfo=utc), max_length=255, verbose_name='title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='room',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.Room'),
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
