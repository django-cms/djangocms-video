# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models.pluginmodel


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(serialize=False, parent_link=True, auto_created=True, to='cms.CMSPlugin', primary_key=True)),
                ('movie', models.FileField(help_text='use .flv file or h264 encoded video file', blank=True, null=True, upload_to=cms.models.pluginmodel.get_plugin_media_path, verbose_name='movie file')),
                ('movie_url', models.CharField(help_text='vimeo or youtube video url. Example: http://www.youtube.com/watch?v=-iJ7bs4mTUY', blank=True, null=True, max_length=255, verbose_name='movie url')),
                ('image', models.ImageField(help_text='preview image file', blank=True, null=True, upload_to=cms.models.pluginmodel.get_plugin_media_path, verbose_name='image')),
                ('width', models.PositiveSmallIntegerField(verbose_name='width')),
                ('height', models.PositiveSmallIntegerField(verbose_name='height')),
                ('auto_play', models.BooleanField(verbose_name='auto play', default=False)),
                ('auto_hide', models.BooleanField(verbose_name='auto hide', default=False)),
                ('fullscreen', models.BooleanField(verbose_name='fullscreen', default=True)),
                ('loop', models.BooleanField(verbose_name='loop', default=False)),
                ('bgcolor', models.CharField(help_text='Hexadecimal, eg ff00cc', default='000000', max_length=6, verbose_name='background color')),
                ('textcolor', models.CharField(help_text='Hexadecimal, eg ff00cc', default='FFFFFF', max_length=6, verbose_name='text color')),
                ('seekbarcolor', models.CharField(help_text='Hexadecimal, eg ff00cc', default='13ABEC', max_length=6, verbose_name='seekbar color')),
                ('seekbarbgcolor', models.CharField(help_text='Hexadecimal, eg ff00cc', default='333333', max_length=6, verbose_name='seekbar bg color')),
                ('loadingbarcolor', models.CharField(help_text='Hexadecimal, eg ff00cc', default='828282', max_length=6, verbose_name='loadingbar color')),
                ('buttonoutcolor', models.CharField(help_text='Hexadecimal, eg ff00cc', default='333333', max_length=6, verbose_name='button out color')),
                ('buttonovercolor', models.CharField(help_text='Hexadecimal, eg ff00cc', default='000000', max_length=6, verbose_name='button over color')),
                ('buttonhighlightcolor', models.CharField(help_text='Hexadecimal, eg ff00cc', default='FFFFFF', max_length=6, verbose_name='button highlight color')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
