# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import django.db.models.deletion
import djangocms_attributes_field.fields


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
            field=models.CharField(default='default', max_length=255, verbose_name='Template', choices=[('default', 'Default')]),
        ),
        migrations.AlterField(
            model_name='videoplayer',
            name='embed_link',
            field=models.CharField(help_text='Use this field to embed videos from external services such as YouTube, Vimeo or others. Leave it blank to upload video files by adding nested "Source" plugins.', max_length=255, verbose_name='Embed link', blank=True),
        ),
        migrations.CreateModel(
            name='VideoSource',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_video_videosource', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
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
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_video_videotrack', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
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
