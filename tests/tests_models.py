# -*- coding: utf-8 -*-
from django.test import TestCase

from djangocms_video.models import VideoPlayer


EXAMPLE_VIDEO = 'http://www.youtube.com/watch?v=-iJ7bs4mTUY'


class VideoTestCase(TestCase):

    def setUp(self):
        VideoPlayer.objects.create(
            template='default',
            embed_link=EXAMPLE_VIDEO,
        )

    def test_video_instance(self):
        """Video player instance has been created"""
        video = VideoPlayer.objects.get(embed_link=EXAMPLE_VIDEO)
        self.assertEqual(video.embed_link, EXAMPLE_VIDEO)
