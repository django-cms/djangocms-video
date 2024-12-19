from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from . import forms, models

DEFAULT_HLSJS_SOURCE = 'https://cdn.jsdelivr.net/npm/hls.js@1.5.17/dist/hls.min.js'

class VideoPlayerPlugin(CMSPluginBase):
    model = models.VideoPlayer
    name = _('Video player')
    text_enabled = True
    allow_children = True
    child_classes = ['VideoSourcePlugin', 'VideoTrackPlugin', 'HlsStreamSourcePlugin']
    form = forms.VideoPlayerPluginForm

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
                'parameters',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'poster',
                'attributes',
                'show_controls',
                'autoplay',
            )
        })
    ]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['video_template'] = instance.template
        context['show_controls'] = instance.show_controls
        context['autoplay'] = instance.autoplay
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
        return 'djangocms_video/{}/source.html'.format(context.get('video_template', 'default'))


class HlsStreamSourcePlugin(CMSPluginBase):
    model = models.HlsStreamSource
    name = _('HLS Stream Source')
    module = _('Video player')
    require_parent = True
    parent_classes = ['VideoPlayerPlugin']

    fieldsets = [
        (None, {
            'fields': (
                'hls_source_url',
            )
        }),
    ]

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        context['source_id'] = instance.id
        context['hlsjs_source'] = getattr(settings, 'DJANGOCMS_VIDEO_HLSJS_SOURCE', DEFAULT_HLSJS_SOURCE)
        return context

    def get_render_template(self, context, instance, placeholder):
        return 'djangocms_video/{}/hls_stream_source.html'.format(context.get('video_template', 'default'))


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
        return 'djangocms_video/{}/track.html'.format(context.get('video_template', 'default'))


plugin_pool.register_plugin(VideoPlayerPlugin)
plugin_pool.register_plugin(HlsStreamSourcePlugin)
plugin_pool.register_plugin(VideoSourcePlugin)
plugin_pool.register_plugin(VideoTrackPlugin)
