# -*- coding: utf-8 -*-
from django.test import TestCase

from djangocms_video.forms import YOUTUBE_EMBED_URL, VideoPlayerPluginForm


class VideoFormTestCase(TestCase):

    def setUp(self):
        self.form_data = {'template': 'default'}

    def test_embed_link_validation(self):
        base_urls = [
            '//youtube.com',
            '//www.youtube.com',

            'http://youtube.com',
            'http://www.youtube.com',

            'https://youtube.com',
            'https://www.youtube.com',
        ]

        url_patterns_flexible_base = [
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

        url_patterns_specific = [
            'http://youtu.be/{id}',
            'http://youtu.be/{id}?feature=youtube_gdata_player',

            '//www.youtube-nocookie.com/embed/{id}?rel=0',
        ]

        video_id = 'NbsRVfLCE1U'
        form_data = self.form_data

        def test_url(video_url):
            form_data['embed_link'] = video_url
            form = VideoPlayerPluginForm(data=form_data)
            self.assertTrue(form.is_valid())
            self.assertEqual(
                form.cleaned_data['embed_link'],
                YOUTUBE_EMBED_URL.format(video_id),
            )

        for base_url in base_urls:
            for url_pattern in url_patterns_flexible_base:
                url = url_pattern.format(
                    base=base_url,
                    id=video_id
                )
                test_url(url)

        for url_pattern in url_patterns_specific:
            url = url_pattern.format(
                id=video_id
            )
            test_url(url)
