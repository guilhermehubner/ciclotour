# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-30 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0013_route_shared_with'),
        ('core', '0005_customuser_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='pending_routes',
            field=models.ManyToManyField(related_name='pending_routes', to='routes.Route'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='performed_routes',
            field=models.ManyToManyField(related_name='performed_routes', to='routes.Route'),
        ),
    ]
