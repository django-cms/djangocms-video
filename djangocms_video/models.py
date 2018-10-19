# -*- coding: utf-8 -*-
"""
Enables the user to add a "Video player" plugin that can render content
from external resources through an embed link or upload single files as
sources to be displayed in an HTML5 player.
"""
import sys

from cms.models import CMSPlugin
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext
from django.utils.translation import ugettext_lazy as _
from djangocms_attributes_field.fields import AttributesField
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

if sys.version_info.major < 3:
    from urlparse import urlparse, parse_qsl, urlunparse
    from urllib import urlencode
else:
    from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

# mp4, are required for full browser support
ALLOWED_EXTENSIONS = getattr(
    settings,
    'DJANGOCMS_VIDEO_ALLOWED_EXTENSIONS',
    ['mp4', 'webm', 'ogv'],
)


# Add additional choices through the ``settings.py``.
def get_templates():
    return [
        ('default', _('Default')),
    ] + getattr(
        settings,
        'DJANGOCMS_VIDEO_TEMPLATES',
        [],
    )


@python_2_unicode_compatible
class VideoPlayer(CMSPlugin):
    """
    Renders either an Iframe when ``link`` is provided or the HTML5 <video> tag
    """
    template = models.CharField(
        verbose_name=_('Template'),
        choices=get_templates(),
        default=get_templates()[0][0],
        max_length=255,
    )
    label = models.CharField(
        verbose_name=_('Label'),
        blank=True,
        max_length=255,
    )
    embed_link = models.CharField(
        verbose_name=_('Embed link'),
        blank=True,
        max_length=255,
        help_text=_(
            'Use this field to embed videos from external services '
            'such as YouTube, Vimeo or others. Leave it blank to upload video '
            'files by adding nested "Source" plugins.'
        ),
    )
    parameters = AttributesField(
        verbose_name=_('Parameters'),
        blank=True,
        help_text=_(
            'Parameters are appended to the video link if provided.'
        ),
    )
    poster = FilerImageField(
        verbose_name=_('Poster'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
    )

    # Add an app namespace to related_name to avoid field name clashes
    # with any other plugins that have a field with the same name as the
    # lowercase of the class name of this model.
    # https://github.com/divio/django-cms/issues/5030
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin,
        related_name='%(app_label)s_%(class)s',
        parent_link=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.label or self.embed_link or str(self.pk)

    def copy_relations(self, oldinstance):
        # Because we have a ForeignKey, it's required to copy over
        # the reference from the instance to the new plugin.
        self.poster = oldinstance.poster

    @property
    def embed_link_with_parameters(self):
        if not self.embed_link:
            return ''
        if not self.parameters:
            return self.embed_link
        return self._append_url_parameters(self.embed_link, self.parameters)

    def _append_url_parameters(self, url, params):
        url_parts = list(urlparse(url))
        query = dict(parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)


@python_2_unicode_compatible
class VideoSource(CMSPlugin):
    """
    Renders the HTML <source> element inside of <video>.
    """
    source_file = FilerFileField(
        verbose_name=_('Source'),
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    text_title = models.CharField(
        verbose_name=_('Title'),
        blank=True,
        max_length=255,
    )
    text_description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
    )

    def __str__(self):
        if self.source_file_id and self.source_file.label:
            return self.source_file.label
        return str(self.pk)

    def clean(self):
        if self.source_file and self.source_file.extension not in ALLOWED_EXTENSIONS:
            raise ValidationError(
                ugettext('Incorrect file type: {extension}.')
                .format(extension=self.source_file.extension)
            )

    def get_short_description(self):
        if self.source_file_id and self.source_file.label:
            return self.source_file.label
        return ugettext('<file is missing>')

    def copy_relations(self, oldinstance):
        # Because we have a ForeignKey, it's required to copy over
        # the reference from the instance to the new plugin.
        self.source_file = oldinstance.source_file


@python_2_unicode_compatible
class VideoTrack(CMSPlugin):
    """
    Renders the HTML <track> element inside <video>.
    """
    KIND_CHOICES = [
        ('subtitles', _('Subtitles')),
        ('captions', _('Captions')),
        ('descriptions', _('Descriptions')),
        ('chapters', _('Chapters')),
    ]

    kind = models.CharField(
        verbose_name=_('Kind'),
        choices=KIND_CHOICES,
        max_length=255,
    )
    src = FilerFileField(
        verbose_name=_('Source file'),
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    srclang = models.CharField(
        verbose_name=_('Source language'),
        blank=True,
        max_length=255,
        help_text=_('Examples: "en" or "de" etc.'),
    )
    label = models.CharField(
        verbose_name=_('Label'),
        blank=True,
        max_length=255,
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
    )

    def __str__(self):
        label = self.kind
        if self.srclang:
            label += ' {}'.format(self.srclang)
        return label
