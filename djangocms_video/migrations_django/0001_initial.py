# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import cms.models.pluginmodel


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('movie', models.FileField(help_text='use .flv file or h264 encoded video file', upload_to=cms.models.pluginmodel.get_plugin_media_path, null=True, verbose_name='movie file', blank=True)),
                ('movie_url', models.CharField(help_text='vimeo or youtube video url. Example: http://www.youtube.com/watch?v=-iJ7bs4mTUY', max_length=255, null=True, verbose_name='movie url', blank=True)),
                ('image', models.ImageField(help_text='preview image file', upload_to=cms.models.pluginmodel.get_plugin_media_path, null=True, verbose_name='image', blank=True)),
                ('width', models.PositiveSmallIntegerField(verbose_name='width')),
                ('height', models.PositiveSmallIntegerField(verbose_name='height')),
                ('auto_play', models.BooleanField(default=False, verbose_name='auto play')),
                ('auto_hide', models.BooleanField(default=False, verbose_name='auto hide')),
                ('fullscreen', models.BooleanField(default=True, verbose_name='fullscreen')),
                ('loop', models.BooleanField(default=False, verbose_name='loop')),
                ('bgcolor', models.CharField(default=b'000000', help_text='Hexadecimal, eg ff00cc', max_length=6, verbose_name='background color')),
                ('textcolor', models.CharField(default=b'FFFFFF', help_text='Hexadecimal, eg ff00cc', max_length=6, verbose_name='text color')),
                ('seekbarcolor', models.CharField(default=b'13ABEC', help_text='Hexadecimal, eg ff00cc', max_length=6, verbose_name='seekbar color')),
                ('seekbarbgcolor', models.CharField(default=b'333333', help_text='Hexadecimal, eg ff00cc', max_length=6, verbose_name='seekbar bg color')),
                ('loadingbarcolor', models.CharField(default=b'828282', help_text='Hexadecimal, eg ff00cc', max_length=6, verbose_name='loadingbar color')),
                ('buttonoutcolor', models.CharField(default=b'333333', help_text='Hexadecimal, eg ff00cc', max_length=6, verbose_name='button out color')),
                ('buttonovercolor', models.CharField(default=b'000000', help_text='Hexadecimal, eg ff00cc', max_length=6, verbose_name='button over color')),
                ('buttonhighlightcolor', models.CharField(default=b'FFFFFF', help_text='Hexadecimal, eg ff00cc', max_length=6, verbose_name='button highlight color')),
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
