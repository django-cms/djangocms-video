# -*- coding: utf-8 -*-

from django import forms
from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        exclude = ('page', 'position', 'placeholder', 'language',
                   'plugin_type')
