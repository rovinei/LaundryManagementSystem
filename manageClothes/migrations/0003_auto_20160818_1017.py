# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-18 03:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manageClothes', '0002_auto_20160818_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundryschedule',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodations.Accommodation'),
        ),
    ]