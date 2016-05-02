# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-02 05:47
from __future__ import unicode_literals

import ciclotour.routes.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('routes', '0005_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutePicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=255, upload_to=ciclotour.routes.models._route_picture_directory_path)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Route')),
            ],
        ),
    ]
