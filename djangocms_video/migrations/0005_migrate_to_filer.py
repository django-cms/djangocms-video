# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


def migrate_to_filer(apps, schema_editor):
    # Because filer is polymorphic, Djangos migration can't handle
    from filer.utils.loader import load_model

    Image = load_model(settings.FILER_IMAGE_MODEL)
    VideoPlayer = apps.get_model('djangocms_video', 'VideoPlayer')
    plugins = VideoPlayer.objects.all()

    for video in plugins:
        if video.image:
            poster = Image.objects.get_or_create(
                file=video.image.file,
                defaults={
                    'name': video.image.name
                }
            )[0]
            plugins.filter(pk=video.pk).update(poster=poster)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('djangocms_video', '0004_move_to_attributes'),
    ]

    operations = [
        migrations.RunPython(migrate_to_filer),
    ]
