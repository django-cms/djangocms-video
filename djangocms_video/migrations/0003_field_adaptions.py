# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import djangocms_attributes_field.fields
import filer.fields.image
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('djangocms_video', '0002_set_related_name_for_cmsplugin_ptr'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Video',
            new_name='VideoPlayer',
        ),
        migrations.AlterField(
            model_name='videoplayer',
            name='cmsplugin_ptr',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='djangocms_video_videoplayer', primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.RenameField(
            model_name='videoplayer',
            old_name='movie_url',
            new_name='embed_link',
        ),
        migrations.AddField(
            model_name='videoplayer',
            name='poster',
            field=filer.fields.image.FilerImageField(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Poster', blank=True, to=settings.FILER_IMAGE_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='videoplayer',
            name='attributes',
            field=djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True),
        ),
    ]
