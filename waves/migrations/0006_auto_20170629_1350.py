# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 13:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waves', '0005_auto_20170629_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='status',
        ),
        migrations.AddField(
            model_name='job',
            name='_status',
            field=models.IntegerField(choices=[(-1, 'Undefined'), (0, 'Created'), (1, 'Prepared'), (2, 'Queued'), (3, 'Running'), (4, 'Suspended'), (5, 'Run completed'), (6, 'Completed'), (7, 'Cancelled'), (9, 'Error')], default=0, verbose_name='Job status'),
        ),
    ]
