# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def reset_null_values(apps, schema_editor):
    VideoPlayer = apps.get_model('djangocms_video', 'VideoPlayer')
    plugins = VideoPlayer.objects.all()
    plugins.filter(embed_link__isnull=True).update(embed_link='')


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_video', '0007_create_nested_plugin'),
    ]

    operations = [
        migrations.RunPython(reset_null_values),
    ]
