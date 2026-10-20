import re
from urllib.parse import parse_qsl, urlencode

from django import forms
from django.conf import settings

from . import models

YOUTUBE_URL_RE = re.compile(r'(?:(?:http://|https://|//)?(?:www\.)?youtu\.?be.*).*')
# https://stackoverflow.com/a/9102270
YOUTUBE_VIDEO_ID_RE = re.compile(r'(?:[?&]v=|/embed/|/1/|/v/|https?://(?:www\.)?youtu\.be/)([^&\n?#]+)')
DEFAULT_YOUTUBE_EMBED_URL = '//www.youtube.com/embed/{}'

VIMEO_URL_RE = re.compile(
    r"(?:https?://|//)?(?:www\.)?vimeo\.com/(?P<video_id>[0-9]+)"
    r"(?:/(?P<privacy_hash>[0-9a-f]+))?/?(?P<query>\?[^#]*)?(?P<fragment>#.*)?",
    re.IGNORECASE,
)


class VideoPlayerPluginForm(forms.ModelForm):
    class Meta:
        model = models.VideoPlayer
        exclude = []
        widgets = {"embed_link": forms.TextInput}

    def clean_embed_link(self):
        link = self.cleaned_data['embed_link']
        # let's check if it's a youtube url
        # (the low cost version)
        if YOUTUBE_URL_RE.match(link):
            # try to get the video id
            results = YOUTUBE_VIDEO_ID_RE.findall(link)
            if results:
                embed_url = getattr(settings, "DJANGOCMS_VIDEO_YOUTUBE_EMBED_URL", DEFAULT_YOUTUBE_EMBED_URL)
                link = embed_url.format(results[0])
        match = VIMEO_URL_RE.fullmatch(link)
        if match:
            query = match["query"] or ""
            if match["privacy_hash"]:
                # Unlisted videos need their privacy hash in the player URL.
                parameters = parse_qsl(query[1:], keep_blank_values=True)
                parameters = [("h", match["privacy_hash"])] + [(key, value) for key, value in parameters if key != "h"]
                query = "?" + urlencode(parameters)
            link = "https://player.vimeo.com/video/{}{}{}".format(match["video_id"], query, match["fragment"] or "")
        return link
