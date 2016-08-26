# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models.pluginmodel
from django.conf import settings


# settings does not exist anymore in 2.x
VIDEO_AUTOPLAY = getattr(settings, "VIDEO_AUTOPLAY", False)
VIDEO_AUTOHIDE = getattr(settings, "VIDEO_AUTOHIDE", False)
VIDEO_FULLSCREEN = getattr(settings, "VIDEO_FULLSCREEN", True)
VIDEO_LOOP = getattr(settings, "VIDEO_LOOP", False)
VIDEO_AUTOPLAY = getattr(settings, "VIDEO_AUTOPLAY", False)
VIDEO_AUTOPLAY = getattr(settings, "VIDEO_AUTOPLAY", False)

VIDEO_BG_COLOR = getattr(settings, "VIDEO_BG_COLOR", "000000")
VIDEO_TEXT_COLOR = getattr(settings, "VIDEO_TEXT_COLOR", "FFFFFF")
VIDEO_SEEKBAR_COLOR = getattr(settings, "VIDEO_SEEKBAR_COLOR", "13ABEC")
VIDEO_SEEKBARBG_COLOR = getattr(settings, "VIDEO_SEEKBARBG_COLOR", "333333")
VIDEO_LOADINGBAR_COLOR = getattr(settings, "VIDEO_LOADINGBAR_COLOR", "828282")
VIDEO_BUTTON_OUT_COLOR = getattr(settings, "VIDEO_BUTTON_OUT_COLOR", "333333")
VIDEO_BUTTON_OVER_COLOR = getattr(settings, "VIDEO_BUTTON_OVER_COLOR", "000000")
VIDEO_BUTTON_HIGHLIGHT_COLOR = getattr(
    settings, "VIDEO_BUTTON_HIGHLIGHT_COLOR", "FFFFFF")

VIDEO_PLUGIN_ENABLE_ADVANCED_SETTINGS = getattr(
    settings, "VIDEO_PLUGIN_ENABLE_ADVANCED_SETTINGS", True)


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(primary_key=True, to='cms.CMSPlugin', auto_created=True, parent_link=True, serialize=False)),
                ('movie', models.FileField(null=True, verbose_name='movie file', upload_to=cms.models.pluginmodel.get_plugin_media_path, help_text='use .flv file or h264 encoded video file', blank=True)),
                ('movie_url', models.CharField(max_length=255, null=True, help_text='vimeo or youtube video url. Example: http://www.youtube.com/watch?v=-iJ7bs4mTUY', blank=True, verbose_name='movie url')),
                ('image', models.ImageField(null=True, verbose_name='image', upload_to=cms.models.pluginmodel.get_plugin_media_path, help_text='preview image file', blank=True)),
                ('width', models.PositiveSmallIntegerField(verbose_name='width')),
                ('height', models.PositiveSmallIntegerField(verbose_name='height')),
                ('auto_play', models.BooleanField(default=VIDEO_AUTOPLAY, verbose_name='auto play')),
                ('auto_hide', models.BooleanField(default=VIDEO_AUTOHIDE, verbose_name='auto hide')),
                ('fullscreen', models.BooleanField(default=VIDEO_FULLSCREEN, verbose_name='fullscreen')),
                ('loop', models.BooleanField(default=VIDEO_LOOP, verbose_name='loop')),
                ('bgcolor', models.CharField(max_length=6, default=VIDEO_BG_COLOR, help_text='Hexadecimal, eg ff00cc', verbose_name='background color')),
                ('textcolor', models.CharField(max_length=6, default=VIDEO_TEXT_COLOR, help_text='Hexadecimal, eg ff00cc', verbose_name='text color')),
                ('seekbarcolor', models.CharField(max_length=6, default=VIDEO_SEEKBAR_COLOR, help_text='Hexadecimal, eg ff00cc', verbose_name='seekbar color')),
                ('seekbarbgcolor', models.CharField(max_length=6, default=VIDEO_SEEKBARBG_COLOR, help_text='Hexadecimal, eg ff00cc', verbose_name='seekbar bg color')),
                ('loadingbarcolor', models.CharField(max_length=6, default=VIDEO_LOADINGBAR_COLOR, help_text='Hexadecimal, eg ff00cc', verbose_name='loadingbar color')),
                ('buttonoutcolor', models.CharField(max_length=6, default=VIDEO_BUTTON_OUT_COLOR, help_text='Hexadecimal, eg ff00cc', verbose_name='button out color')),
                ('buttonovercolor', models.CharField(max_length=6, default=VIDEO_BUTTON_OVER_COLOR, help_text='Hexadecimal, eg ff00cc', verbose_name='button over color')),
                ('buttonhighlightcolor', models.CharField(max_length=6, default=VIDEO_BUTTON_HIGHLIGHT_COLOR, help_text='Hexadecimal, eg ff00cc', verbose_name='button highlight color')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
