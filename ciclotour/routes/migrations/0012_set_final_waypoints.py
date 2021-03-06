# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-29 02:36
from __future__ import unicode_literals
from django.db import migrations


def foward_set_final(apps, schema_editor):
    Route = apps.get_model('routes', 'Route')

    for route in Route.objects.all():
        w = route.waypoint_set.all().order_by('id').last()

        if w.kind == 'G':
            w.kind = 'FG'
        else:
            w.kind = 'FL'

        w.save()

def backward_set_final(apps, schema_editor):
    Route = apps.get_model('routes', 'Route')

    for route in Route.objects.all():
        w = route.waypoint_set.all().order_by('id').last()

        if w.kind == 'FG':
            w.kind = 'G'
        else:
            w.kind = 'L'

        w.save()

class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0011_auto_20160529_0259'),
    ]

    operations = [
        migrations.RunPython(foward_set_final, backward_set_final)
    ]
