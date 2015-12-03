# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import settings
from .forms import VideoForm
from .models import Video


class VideoPlugin(CMSPluginBase):
    model = Video
    name = _("Video")
    form = VideoForm
    text_enabled = True

    render_template = "cms/plugins/video.html"

    general_fields = [
        ('movie', 'movie_url'),
        'image',
        ('width', 'height'),
        'auto_play',
        'auto_hide',
        'fullscreen',
        'loop',
    ]
    color_fields = [
        'bgcolor',
        'textcolor',
        'seekbarcolor',
        'seekbarbgcolor',
        'loadingbarcolor',
        'buttonoutcolor',
        'buttonovercolor',
        'buttonhighlightcolor',
    ]

    fieldsets = [
        (None, {
            'fields': general_fields,
        }),
    ]
    if settings.VIDEO_PLUGIN_ENABLE_ADVANCED_SETTINGS:
        fieldsets += [
            (_('Color Settings'), {
                'fields': color_fields,
                'classes': ('collapse',),
            }),
        ]

    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder': placeholder,
        })
        return context

plugin_pool.register_plugin(VideoPlugin)
