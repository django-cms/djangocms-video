from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase

from djangocms_video.models import (
    VideoPlayer, VideoSource, VideoTrack, get_extensions, get_templates,
)

from .helpers import get_filer_file, get_filer_image


class VideoModelsTestCase(TestCase):

    def setUp(self):
        self.embed_link = "http://www.youtube.com/watch?v=-wVD1eIrQoQs"
        self.picture = get_filer_image()
        self.video_file = get_filer_file(file_name="test_video.mp4")

    def tearDown(self):
        if self.picture:
            self.picture.delete()
            del self.picture
            with self.assertRaises(AttributeError):
                print(self.picture)
        if self.video_file:
            self.video_file.delete()
            del self.video_file
            with self.assertRaises(AttributeError):
                print(self.video_file)

        VideoPlayer.objects.filter(pk=1).delete()
        self.assertEqual(len(VideoPlayer.objects.all()), 0)
        VideoSource.objects.filter(pk=1).delete()
        self.assertEqual(len(VideoSource.objects.all()), 0)
        VideoTrack.objects.filter(pk=1).delete()
        self.assertEqual(len(VideoTrack.objects.all()), 0)

    def test_settings(self):
        self.assertEqual(get_extensions(), ['mp4', 'webm', 'ogv'])
        settings.DJANGOCMS_VIDEO_ALLOWED_EXTENSIONS = ['mp4', 'flv']
        self.assertEqual(get_extensions(), ['mp4', 'flv'])

        self.assertEqual(get_templates(), [('default', 'Default')])
        settings.DJANGOCMS_VIDEO_TEMPLATES = [('feature', 'Feature')]
        self.assertEqual(get_templates(), [('default', 'Default'), ('feature', 'Feature')])

    def test_video_instance(self):
        VideoPlayer.objects.create(
            template="default",
            label="test label",
            parameters="{'autoplay': 'true'}",
            poster=self.picture,
            embed_link=self.embed_link,
            attributes="{'data-type', 'video'}",
        )
        instance = VideoPlayer.objects.all()
        self.assertEqual(len(instance), 1)
        instance = VideoPlayer.objects.get(pk=1)
        self.assertEqual(instance.label, "test label")
        self.assertEqual(instance.parameters, "{'autoplay': 'true'}")
        self.assertEqual(instance.embed_link, self.embed_link)
        self.assertEqual(instance.attributes, "{'data-type', 'video'}")
        self.assertEqual(instance.poster, self.picture)
        # old copy relation
        instance.copy_relations(instance)
        self.assertEqual(instance.embed_link, self.embed_link)
        # test string output
        self.assertEqual(instance.__str__(), "test label")
        instance.label = None
        self.assertEqual(instance.__str__(), self.embed_link)
        instance.embed_link = None
        self.assertEqual(instance.__str__(), "1")

    def test_video_parameters(self):
        instance = VideoPlayer.objects.create(
            template="default",
        )
        self.assertEqual(instance.embed_link_with_parameters, "")
        instance.embed_link = self.embed_link
        self.assertEqual(
            instance.embed_link_with_parameters,
            self.embed_link,
        )
        instance.parameters = {"autoplay": "true"}
        self.assertIn("v=-wVD1eIrQoQs", instance.embed_link_with_parameters)
        self.assertIn("autoplay=true", instance.embed_link_with_parameters)

    def test_video_source_instance(self):
        VideoSource.objects.create(
            source_file=self.video_file,
            text_title="some title",
            text_description="some description",
            attributes="{'data-type', 'track'}"
        )
        instance = VideoSource.objects.all()
        self.assertEqual(len(instance), 1)
        instance = VideoSource.objects.get(pk=1)
        self.assertEqual(instance.source_file, self.video_file)
        self.assertEqual(instance.text_title, "some title")
        self.assertEqual(instance.text_description, "some description")
        self.assertEqual(instance.attributes, "{'data-type', 'track'}")
        self.assertEqual(instance.clean(), None)
        self.assertEqual(instance.get_short_description(), "test_video.mp4")
        # test string output
        self.assertEqual(instance.__str__(), "test_video.mp4")
        instance.source_file = None
        self.assertEqual(instance.__str__(), "1")
        # test not allowed extension
        instance.source_file = get_filer_file("test_file.mp3")
        with self.assertRaises(ValidationError):
            instance.clean()
        instance.source_file = None
        self.assertEqual(instance.get_short_description(), "<file is missing>")
        # old copy relation
        instance.copy_relations(instance)
        self.assertEqual(instance.source_file, None)

    def test_video_track_instance(self):
        VideoTrack.objects.create(
            kind=VideoTrack.KIND_CHOICES[0][0],
            src=self.video_file,  # should be .vtt normally
            srclang="en",
            label="track label",
            attributes="{'data-type, 'video'}",
        )
        instance = VideoTrack.objects.all()
        self.assertEqual(len(instance), 1)
        instance = VideoTrack.objects.get(pk=1)
        self.assertEqual(instance.kind, "subtitles")
        self.assertEqual(instance.src, self.video_file)
        self.assertEqual(instance.srclang, "en")
        self.assertEqual(instance.label, "track label")
        self.assertEqual(instance.attributes, "{'data-type, 'video'}")
        self.assertEqual(instance.__str__(), "subtitles (en)")
        # case when the folder has been removed
        instance.srclang = None
        self.assertEqual(instance.__str__(), "subtitles")
