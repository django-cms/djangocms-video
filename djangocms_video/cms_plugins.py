# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models


class VideoPlayerPlugin(CMSPluginBase):
    model = models.VideoPlayer
    name = _('Video player')
    text_enabled = True
    allow_children = True
    child_classes = ['VideoSourcePlugin', 'VideoTrackPlugin']

    fieldsets = [
        (None, {
            'fields': (
                'template',
                'label',
            )
        }),
        (_('Embed video'), {
            'classes': ('collapse',),
            'fields': (
                'embed_link',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'poster',
                'attributes',
            )
        })
    ]

    def render(self, context, instance, placeholder):
        context = super(VideoPlayerPlugin, self).render(context, instance, placeholder)
        context['video_template'] = instance.template
        return context

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_video/{}/video_player.html'.format(instance.template)


class VideoSourcePlugin(CMSPluginBase):
    model = models.VideoSource
    name = _('Source')
    module = _('Video player')
    require_parent = True
    parent_classes = ['VideoPlayerPlugin']

    fieldsets = [
        (None, {
            'fields': (
                'source_file',
                'text_title',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'text_description',
                'attributes',
            )
        })
    ]

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_video/{}/source.html'.format(context['video_template'])


class VideoTrackPlugin(CMSPluginBase):
    model = models.VideoTrack
    name = _('Track')
    module = _('Video player')
    require_parent = True
    parent_classes = ['VideoPlayerPlugin']

    fieldsets = [
        (None, {
            'fields': (
                'kind',
                'src',
                'srclang',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'label',
                'attributes',
            )
        })
    ]

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_video/{}/track.html'.format(context['video_template'])


plugin_pool.register_plugin(VideoPlayerPlugin)
plugin_pool.register_plugin(VideoSourcePlugin)
plugin_pool.register_plugin(VideoTrackPlugin)
