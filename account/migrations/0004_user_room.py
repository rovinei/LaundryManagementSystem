# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-17 09:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0002_auto_20160817_1546'),
        ('account', '0003_remove_user_accommodation'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='room',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='accommodations.Accommodation'),
        ),
    ]
