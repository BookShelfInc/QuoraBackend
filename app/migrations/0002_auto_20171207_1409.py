# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-07 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentary',
            name='time',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
