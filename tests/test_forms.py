from django.test import TestCase, override_settings

from djangocms_video.forms import (
    DEFAULT_YOUTUBE_EMBED_URL,
    YOUTUBE_URL_RE,
    VideoPlayerPluginForm,
)

YOUTUBE_NOCOOKIE_EMBED_URL = "//www.youtube-nocookie.com/embed/{}"


class VideoFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_urls = [
            '//youtube.com',
            '//www.youtube.com',

            'http://youtube.com',
            'http://www.youtube.com',

            'https://youtube.com',
            'https://www.youtube.com',
        ]

        cls.url_patterns_flexible_base = [
            '{base}/watch?v={id}',
            '{base}/watch?v={id}&feature=channel',
            '{base}/watch?v={id}&playnext_from=TL&videos=osPknwzXEas&feature=sub',
            '{base}/watch?v={id}&feature=youtube_gdata_player',
            '{base}/watch?v={id}&feature=youtu.be',
            '{base}/v/{id}?feature=youtube_gdata_player',

            '{base}/djangocms?v={id}',
            '{base}/user/djangocms#p/u/1/{id}',
            '{base}/user/djangocms#p/u/1/{id}?rel=0',
            '{base}/embed/{id}?rel=0',
        ]

        cls.url_patterns_specific = [
            'http://youtu.be/{id}',
            'http://youtu.be/{id}?feature=youtube_gdata_player',

            '//www.youtube-nocookie.com/embed/{id}?rel=0',
        ]

        cls.video_id = 'NbsRVfLCE1U'

    def setUp(self):
        self.form_data = {'template': 'default'}

    def test_embed_link_validation(self):
        form_data = self.form_data

        def test_url(video_url):
            form_data['embed_link'] = video_url
            form = VideoPlayerPluginForm(data=form_data)
            self.assertTrue(form.is_valid())
            self.assertEqual(
                form.cleaned_data['embed_link'],
                DEFAULT_YOUTUBE_EMBED_URL.format(self.video_id),
            )

        for base_url in self.base_urls:
            for url_pattern in self.url_patterns_flexible_base:
                url = url_pattern.format(
                    base=base_url,
                    id=self.video_id
                )
                test_url(url)

        for url_pattern in self.url_patterns_specific:
            url = url_pattern.format(
                id=self.video_id
            )
            test_url(url)

    @override_settings(DJANGOCMS_VIDEO_YOUTUBE_EMBED_URL=YOUTUBE_NOCOOKIE_EMBED_URL)
    def test_alternative_youtube_link(self):
        form_data = self.form_data

        def test_url(video_url):
            form_data['embed_link'] = video_url
            form = VideoPlayerPluginForm(data=form_data)
            self.assertTrue(form.is_valid())
            self.assertEqual(
                form.cleaned_data['embed_link'],
                YOUTUBE_NOCOOKIE_EMBED_URL.format(self.video_id),
            )

        for base_url in self.base_urls:
            for url_pattern in self.url_patterns_flexible_base:
                url = url_pattern.format(
                    base=base_url,
                    id=self.video_id
                )
                test_url(url)

        for url_pattern in self.url_patterns_specific:
            url = url_pattern.format(
                id=self.video_id
            )
            test_url(url)

    def test_clean_embed_link(self):
        form_data = {'template': 'default'}
        form_data['embed_link'] = "http://www.youtube.com"
        form = VideoPlayerPluginForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data['embed_link'],
            form.clean_embed_link(),
        )
        self.assertTrue(YOUTUBE_URL_RE.match(form.cleaned_data['embed_link']))

        form_data['embed_link'] = "http://www.vimeo.com"
        form = VideoPlayerPluginForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertIsNone(YOUTUBE_URL_RE.match(form.cleaned_data['embed_link']))
