# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_videosourceplugin(apps, schema_editor):
    from cms import api
    from cms.models import Placeholder, CMSPlugin
    from filer.models import File

    VideoPlayer = apps.get_model('djangocms_video', 'VideoPlayer')
    plugins = VideoPlayer.objects.all()

    for video in plugins:
        # adapt plugin name
        plugins.filter(pk=video.pk).update(plugin_type='VideoPlayerPlugin')
        # add nested video source plugin
        if video.movie:
            placeholder = Placeholder.objects.get(pk=video.placeholder_id)
            target = CMSPlugin.objects.get(pk=video.pk)
            image = File.objects.get_or_create(
                file=video.movie.file,
                defaults={
                    'name': video.movie.name
                }
            )[0]

            plugin = api.add_plugin(
                language=video.language,
                placeholder=placeholder,
                plugin_type='VideoSourcePlugin',
                position='last-child',
                target=target,
                # video source fields
                source_file=image
            )


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_video', '0006_field_adaptions'),
    ]

    operations = [
        migrations.RunPython(create_videosourceplugin),
        migrations.RemoveField(
            model_name='videoplayer',
            name='movie',
        ),
    ]
