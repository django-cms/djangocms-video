from cms.api import add_plugin, create_page
from cms.test_utils.testcases import CMSTestCase

from djangocms_video.cms_plugins import (
    VideoPlayerPlugin, VideoSourcePlugin, VideoTrackPlugin,
)

from .helpers import get_filer_file


class VideoPlayerPluginsTestCase(CMSTestCase):

    def setUp(self):
        self.language = "en"
        self.home = create_page(
            title='home',
            template='page.html',
            language=self.language,
        )
        self.home.publish(self.language)
        self.page = create_page(
            title='content',
            template='page.html',
            language=self.language,
        )
        self.page.publish(self.language)
        self.placeholder = self.page.placeholders.get(slot="content")
        self.superuser = self.get_superuser()
        self.video_file = get_filer_file("test_file.mp4")
        self.track_file = get_filer_file("test_track.vtt")

    def tearDown(self):
        self.page.delete()
        self.home.delete()
        self.superuser.delete()
        self.video_file.delete()
        self.track_file.delete()

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
        request_url = self.page.get_absolute_url(self.language) + "?toolbar_off=true"

        parent = add_plugin(
            placeholder=self.placeholder,
            plugin_type=VideoPlayerPlugin.__name__,
            language=self.language,
            template="default",
        )
        self.page.publish(self.language)
        self.assertEqual(parent.get_plugin_class_instance().name, "Video player")

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertIn(b"Your browser doesn't support this video format.", response.content)

        child = add_plugin(
            target=parent,
            placeholder=self.placeholder,
            plugin_type=VideoSourcePlugin.__name__,
            language=self.language,
            source_file=self.video_file,
        )
        self.page.publish(self.language)
        self.assertEqual(child.source_file.label, "test_file.mp4")

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

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
        self.page.publish(self.language)
        self.assertEqual(track.src.label, "test_track.vtt")

        with self.login_user_context(self.superuser):
            response = self.client.get(request_url)

        self.assertIn(b"<track kind", response.content)
        self.assertContains(response, self.track_file.label)
