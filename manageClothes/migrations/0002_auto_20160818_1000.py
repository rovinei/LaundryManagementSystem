# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-08-18 03:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accommodations', '0002_auto_20160817_1546'),
        ('manageClothes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaundrySchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('M', 'Monday'), ('TUE', 'Tuesday'), ('WED', 'Wednesday'), ('THU', 'Thursday'), ('FRI', 'Friday'), ('SAT', 'Saturday'), ('SUN', 'Sunday')], max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accommodations.Accommodation', unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='laundryschedule',
            unique_together=set([('room', 'day')]),
        ),
    ]