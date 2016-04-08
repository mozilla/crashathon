# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crash',
            options={
                'db_table': 'crash',
            },
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.UUIDField()),
                ('app_version', models.CharField(max_length=8)),
                ('creation_date', models.DateTimeField()),
                ('geo_country', models.CharField(max_length=2)),
            ],
        ),
    ]
