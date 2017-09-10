# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20170628_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='subjects',
        ),
        migrations.AlterField(
            model_name='profile',
            name='classSize',
            field=models.IntegerField(choices=[(1, '0-5'), (2, '6-10'), (3, '11-15'), (4, '16-20'), (5, '21-25'), (6, '25+')], null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='hardware_devices',
            field=models.ManyToManyField(blank=True, to='website.Hardware'),
        ),
        migrations.AddField(
            model_name='profile',
            name='subjectsTaught',
            field=models.ManyToManyField(blank=True, to='website.Subject'),
        ),
    ]
