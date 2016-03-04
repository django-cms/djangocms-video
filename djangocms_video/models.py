# -*- coding: utf-8 -*-

import os

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
try:
    from cms.models import get_plugin_media_path
except ImportError:
    def get_plugin_media_path(instance, filename):
        """
        See cms.models.pluginmodel.get_plugin_media_path on django CMS 3.0.4+
        for information
        """
        return instance.get_media_path(filename)
from cms.utils.compat.dj import python_2_unicode_compatible

from . import settings


@python_2_unicode_compatible
class Video(CMSPlugin):
    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='djangocms_video_video', parent_link=True)

    # player settings
    movie = models.FileField(
        _('movie file'), upload_to=get_plugin_media_path,
        help_text=_('use .flv file or h264 encoded video file'), blank=True,
        null=True)

    movie_url = models.CharField(
        _('movie url'), max_length=255,
        help_text=_('vimeo or youtube video url. '
                    'Example: http://www.youtube.com/watch?v=-iJ7bs4mTUY'),
        blank=True, null=True)

    image = models.ImageField(
        _('image'), upload_to=get_plugin_media_path,
        help_text=_('preview image file'), null=True, blank=True)

    width = models.PositiveSmallIntegerField(_('width'))

    height = models.PositiveSmallIntegerField(_('height'))

    auto_play = models.BooleanField(
        _('auto play'), default=settings.VIDEO_AUTOPLAY)

    auto_hide = models.BooleanField(
        _('auto hide'), default=settings.VIDEO_AUTOHIDE)

    fullscreen = models.BooleanField(
        _('fullscreen'), default=settings.VIDEO_FULLSCREEN)

    loop = models.BooleanField(_('loop'), default=settings.VIDEO_LOOP)

    # plugin settings
    bgcolor = models.CharField(
        _('background color'), max_length=6, default=settings.VIDEO_BG_COLOR,
        help_text=_('Hexadecimal, eg ff00cc'))

    textcolor = models.CharField(
        _('text color'), max_length=6, default=settings.VIDEO_TEXT_COLOR,
        help_text=_('Hexadecimal, eg ff00cc'))

    seekbarcolor = models.CharField(
        _('seekbar color'), max_length=6, default=settings.VIDEO_SEEKBAR_COLOR,
        help_text=_('Hexadecimal, eg ff00cc'))

    seekbarbgcolor = models.CharField(
        _('seekbar bg color'), max_length=6,
        default=settings.VIDEO_SEEKBARBG_COLOR,
        help_text=_('Hexadecimal, eg ff00cc'))

    loadingbarcolor = models.CharField(
        _('loadingbar color'), max_length=6,
        default=settings.VIDEO_LOADINGBAR_COLOR,
        help_text=_('Hexadecimal, eg ff00cc'))

    buttonoutcolor = models.CharField(
        _('button out color'), max_length=6,
        default=settings.VIDEO_BUTTON_OUT_COLOR,
        help_text=_('Hexadecimal, eg ff00cc'))

    buttonovercolor = models.CharField(
        _('button over color'), max_length=6,
        default=settings.VIDEO_BUTTON_OVER_COLOR,
        help_text=_('Hexadecimal, eg ff00cc'))

    buttonhighlightcolor = models.CharField(
        _('button highlight color'), max_length=6,
        default=settings.VIDEO_BUTTON_HIGHLIGHT_COLOR,
        help_text=_('Hexadecimal, eg ff00cc'))

    def __str__(self):
        if self.movie:
            name = self.movie.path
        else:
            name = self.movie_url
        return u"%s" % os.path.basename(name)

    def get_height(self):
        return "%s" % self.height

    def get_width(self):
        return "%s" % self.width

    def get_movie(self):
        if self.movie:
            return self.movie.url
        else:
            return self.movie_url
