# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-29 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0010_auto_20160508_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='waypoint',
            name='kind',
            field=models.CharField(choices=[('I', 'Inicial'), ('L', 'Linear'), ('G', 'Google'), ('FG', 'Final Google'), ('FL', 'Final Linear')], max_length=2),
        ),
    ]
