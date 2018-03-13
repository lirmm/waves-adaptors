# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-13 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wavesapiuser',
            options={'verbose_name': 'Waves Api auth', 'verbose_name_plural': 'Waves Api auths'},
        ),
        migrations.AlterField(
            model_name='wavesapiuser',
            name='domain',
            field=models.CharField(blank=True, help_text='Comma separated list', max_length=255, null=True, verbose_name='Origin URL(s)'),
        ),
        migrations.AlterField(
            model_name='wavesapiuser',
            name='ip_list',
            field=models.CharField(blank=True, help_text='Comma separated list', max_length=255, null=True, verbose_name='Ip(s) List'),
        ),
    ]
