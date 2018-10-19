# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
import djangocms_attributes_field.fields
import filer.fields.file
from django.db import migrations, models

from djangocms_video.models import get_templates


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0006_auto_20160623_1627'),
        ('djangocms_video', '0005_migrate_to_filer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoplayer',
            name='image',
        ),
        migrations.AddField(
            model_name='videoplayer',
            name='label',
            field=models.CharField(max_length=255, verbose_name='Label', blank=True),
        ),
        migrations.AddField(
            model_name='videoplayer',
            name='template',
            field=models.CharField(default=get_templates()[0][0], max_length=255, verbose_name='Template', choices=get_templates()),
        ),
        migrations.CreateModel(
            name='VideoSource',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='djangocms_video_videosource', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('text_title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('text_description', models.TextField(verbose_name='Description', blank=True)),
                ('attributes', djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True)),
                ('source_file', filer.fields.file.FilerFileField(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Source', to='filer.File', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='VideoTrack',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, related_name='djangocms_video_videotrack', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('kind', models.CharField(max_length=255, verbose_name='Kind', choices=[('subtitles', 'Subtitles'), ('captions', 'Captions'), ('descriptions', 'Descriptions'), ('chapters', 'Chapters')])),
                ('srclang', models.CharField(help_text='Examples: "en" or "de" etc.', max_length=255, verbose_name='Source language', blank=True)),
                ('label', models.CharField(max_length=255, verbose_name='Label', blank=True)),
                ('attributes', djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True)),
                ('src', filer.fields.file.FilerFileField(related_name='+', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Source file', to='filer.File', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
