# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-01 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='trial_acc',
            field=models.BooleanField(default=False),
        ),
    ]
