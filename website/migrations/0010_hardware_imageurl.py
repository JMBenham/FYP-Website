# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 02:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_devicequestionnaire_hardware'),
    ]

    operations = [
        migrations.AddField(
            model_name='hardware',
            name='imageUrl',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
