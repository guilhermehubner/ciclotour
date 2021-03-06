# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-06-11 18:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('routes', '0013_route_shared_with'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Route')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-published'],
            },
        ),
    ]
