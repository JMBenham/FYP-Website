# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-28 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20170628_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='classSize',
            field=models.CharField(default=25, max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='hardware_devices',
            field=models.ManyToManyField(to='website.Hardware'),
        ),
        migrations.AddField(
            model_name='profile',
            name='programmingBackground',
            field=models.CharField(default='Expert', max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='subjects',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('MTH', 'Maths'), ('SCI', 'Science'), ('ENG', 'English'), ('ART', 'Art'), ('I.T', 'Information Technology')], max_length=19, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='technologyBackground',
            field=models.CharField(default='Expert', max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='yearLevels',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(0, 'Prep'), (1, 'Grade 1'), (2, 'Grade 2'), (3, 'Grade 3'), (4, 'Grade 4'), (5, 'Grade 5'), (6, 'Grade 6'), (7, 'Year 7'), (8, 'Year 8'), (9, 'Year 9'), (10, 'Year 10'), (11, 'Year 11'), (12, 'Year 12')], max_length=28, null=True),
        ),
    ]
