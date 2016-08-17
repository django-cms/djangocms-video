# -*- coding: utf-8 -*-
from django.test import TestCase
from djangocms_video.models import Video


EXAMPLE_VIDEO = 'http://www.youtube.com/watch?v=-iJ7bs4mTUY'


class VideoTestCase(TestCase):

    def setUp(self):
        Video.objects.create(
            movie_url=EXAMPLE_VIDEO,
            width=200,
            height=200,
        )

    def test_video_instance(self):
        """Video player instance has been created"""
        video = Video.objects.get(movie_url=EXAMPLE_VIDEO)
        self.assertEqual(video.movie_url, EXAMPLE_VIDEO)
