# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-03 11:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manageClothes', '0002_auto_20160803_1807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clothe',
            old_name='tpye',
            new_name='type',
        ),
    ]
