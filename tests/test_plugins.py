from cms.api import add_plugin
from cms.test_utils.testcases import CMSTestCase

from djangocms_video.cms_plugins import (
    VideoPlayerPlugin,
    VideoSourcePlugin,
    VideoTrackPlugin,
)

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
