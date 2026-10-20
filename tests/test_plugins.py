from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase
from django.contrib import admin
from django.template.loader import render_to_string
from django.test import override_settings
from sekizai.context import SekizaiContext

from djangocms_video.cms_plugins import (
    DEFAULT_HLSJS_SOURCE,
    HlsStreamSourcePlugin,
    VideoPlayerPlugin,
    VideoSourcePlugin,
    VideoTrackPlugin,
)
from djangocms_video.forms import VideoPlayerPluginForm
from djangocms_video.models import HlsStreamSource

from .fixtures import TestFixture
from .helpers import get_filer_file


class VideoPlayerPluginsTestCase(TestFixture, CMSTestCase):

    def setUp(self):
        super().setUp()
        self.video_file = get_filer_file("test_file.mp4")
        self.track_file = get_filer_file("test_track.vtt")

    def tearDown(self):
        self.video_file.delete()
        self.track_file.delete()
        super().tearDown()

    def test_player_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=VideoPlayerPlugin.__name__,
            language=self.language,
        )
        self.assertEqual(plugin.plugin_type, "VideoPlayerPlugin")

    def test_source_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=VideoSourcePlugin.__name__,
            language=self.language,
        )
        self.assertEqual(plugin.plugin_type, "VideoSourcePlugin")

    def test_track_plugin(self):
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=VideoTrackPlugin.__name__,
            language=self.language,
        )
        self.assertEqual(plugin.plugin_type, "VideoTrackPlugin")

    def test_hls_stream_source_plugin(self):
        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=VideoPlayerPlugin.__name__,
            language=self.language,
        )
        url = "https://example.com/live/playlist.m3u8"
        child = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=HlsStreamSourcePlugin.__name__,
            language=self.language,
            hls_source_url=url,
        )
        self.assertIsInstance(child, HlsStreamSource)
        self.assertEqual(child.parent_id, parent.pk)
        self.assertIn("HlsStreamSourcePlugin", VideoPlayerPlugin.child_classes)
        self.assertTrue(HlsStreamSourcePlugin.require_parent)
        self.assertEqual(HlsStreamSourcePlugin.parent_classes, ["VideoPlayerPlugin"])
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)
        self.assertContains(response, f'src="{url}" type="application/x-mpegURL"')
        self.assertContains(response, f'<script src="{DEFAULT_HLSJS_SOURCE}"></script>', count=1)

    def test_hls_stream_source_render(self):
        instance = HlsStreamSource(pk=42, hls_source_url="https://example.com/live.m3u8")
        plugin = HlsStreamSourcePlugin(HlsStreamSource, admin.site)
        context = plugin.render(SekizaiContext(), instance, self.placeholder)
        self.assertEqual(context["source_id"], instance.pk)
        self.assertEqual(context["hlsjs_source"], DEFAULT_HLSJS_SOURCE)
        template = plugin.get_render_template(context, instance, self.placeholder)
        self.assertEqual(template, "djangocms_video/default/hls_stream_source.html")
        html = render_to_string(template, context.flatten())
        self.assertHTMLEqual(
            html,
            '<source id="42" src="https://example.com/live.m3u8" type="application/x-mpegURL">',
        )
        self.assertIn(
            f'<script src="{DEFAULT_HLSJS_SOURCE}"></script>',
            "\n".join(context["SEKIZAI_CONTENT_HOLDER"]["js"]),
        )

        second = HlsStreamSource(pk=43, hls_source_url="https://example.com/other.m3u8")
        context = plugin.render(context, second, self.placeholder)
        render_to_string(template, context.flatten())
        scripts = "\n".join(context["SEKIZAI_CONTENT_HOLDER"]["js"])
        self.assertEqual(scripts.count(f'<script src="{DEFAULT_HLSJS_SOURCE}"></script>'), 1)
        self.assertIn("document.getElementById('42')", scripts)
        self.assertIn("document.getElementById('43')", scripts)

        context["video_template"] = "feature"
        self.assertEqual(
            plugin.get_render_template(context, instance, self.placeholder),
            "djangocms_video/feature/hls_stream_source.html",
        )

    @override_settings(DJANGOCMS_VIDEO_HLSJS_SOURCE="/static/js/hls.min.js")
    def test_hls_stream_source_custom_script(self):
        instance = HlsStreamSource(pk=42, hls_source_url="https://example.com/live.m3u8")
        plugin = HlsStreamSourcePlugin(HlsStreamSource, admin.site)
        context = plugin.render(SekizaiContext(), instance, self.placeholder)
        self.assertEqual(context["hlsjs_source"], "/static/js/hls.min.js")
        template = plugin.get_render_template(context, instance, self.placeholder)
        render_to_string(template, context.flatten())
        self.assertIn(
            '<script src="/static/js/hls.min.js"></script>',
            "\n".join(context["SEKIZAI_CONTENT_HOLDER"]["js"]),
        )

    def test_hls_stream_source_disabled(self):
        instance = HlsStreamSource(pk=42, hls_source_url="https://example.com/live.m3u8")
        plugin = HlsStreamSourcePlugin(HlsStreamSource, admin.site)
        context = plugin.render(SekizaiContext({"disabled": True}), instance, self.placeholder)
        template = plugin.get_render_template(context, instance, self.placeholder)
        self.assertEqual(render_to_string(template, context.flatten()).strip(), "")
        self.assertEqual(list(context["SEKIZAI_CONTENT_HOLDER"]["js"]), [])

    def test_player_playback_options(self):
        for show_controls in (True, False):
            for autoplay in (True, False):
                with self.subTest(show_controls=show_controls, autoplay=autoplay):
                    instance = add_plugin(
                        placeholder=self.placeholder,
                        plugin_type=VideoPlayerPlugin.__name__,
                        language=self.language,
                        show_controls=show_controls,
                        autoplay=autoplay,
                    )
                    instance.refresh_from_db()
                    plugin = instance.get_plugin_class_instance()
                    context = plugin.render({}, instance, self.placeholder)
                    template = plugin.get_render_template(context, instance, self.placeholder)
                    html = render_to_string(template, context)
                    controls = " controls" if show_controls else ""
                    autoplay_attr = " autoplay" if autoplay else ""
                    self.assertHTMLEqual(
                        html,
                        '<div class="djangocms-video-plugin">'
                        f"<video{controls}{autoplay_attr}>"
                        "Your browser doesn't support this video format."
                        "</video></div>",
                    )

    def test_plugin_structure(self):
        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=VideoPlayerPlugin.__name__,
            language=self.language,
            template="default",
        )
        self.publish(self.page, self.language)
        self.assertEqual(parent.get_plugin_class_instance().name, "Video player")

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertIn(b"Your browser doesn't support this video format.", response.content)

        child = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=VideoSourcePlugin.__name__,
            language=self.language,
            source_file=self.video_file,
        )
        self.publish(self.page, self.language)
        self.assertEqual(child.source_file.label, "test_file.mp4")

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertIn(b"<video controls", response.content)
        self.assertContains(response, self.video_file.label)

        track = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=VideoTrackPlugin.__name__,
            language=self.language,
            kind="subtitles",
            src=self.track_file,
            srclang=self.language,
        )
        self.publish(self.page, self.language)
        self.assertEqual(track.src.label, "test_track.vtt")

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertIn(b"<track kind", response.content)
        self.assertContains(response, self.track_file.label)

    def test_vimeo_player_rendering(self):
        tracking = "a" * 200
        expected = f"https://player.vimeo.com/video/367756121?h=a75baf7391&tracking={tracking}"
        form = VideoPlayerPluginForm(
            data={
                "template": "default",
                "embed_link": f"https://vimeo.com/367756121/a75baf7391?tracking={tracking}",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        plugin = add_plugin(
            placeholder=self.placeholder,
            plugin_type=VideoPlayerPlugin.__name__,
            language=self.language,
            embed_link=form.cleaned_data["embed_link"],
            parameters={"h": "old", "autoplay": "1"},
        )
        plugin.refresh_from_db()
        self.assertEqual(plugin.embed_link, expected)
        self.publish(self.page, self.language)

        with self.login_user_context(self.superuser):
            response = self.client.get(self.request_url)

        self.assertContains(
            response,
            f'src="https://player.vimeo.com/video/367756121?h=a75baf7391&amp;tracking={tracking}&amp;autoplay=1"',
        )
