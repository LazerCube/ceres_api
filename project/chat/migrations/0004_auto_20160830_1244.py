# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-30 11:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20160829_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='object_id',
            field=models.UUIDField(),
        ),
    ]
