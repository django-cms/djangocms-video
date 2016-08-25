# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion
import djangocms_attributes_field.fields


class Migration(migrations.Migration):

    dependencies = [
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
            field=models.OneToOneField(parent_link=True, related_name='djangocms_video_videoplayer', primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.RenameField(
            model_name='videoplayer',
            old_name='movie_url',
            new_name='embed_link',
        ),
        migrations.AddField(
            model_name='videoplayer',
            name='poster',
            field=filer.fields.image.FilerImageField(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Poster', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='videoplayer',
            name='attributes',
            field=djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True),
        ),
    ]
