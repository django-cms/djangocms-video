# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    templates = forms.CharField(
        'List of additional templates (comma separated)',
        required=False,
    )
    extensions = forms.CharField(
        'List of allowed extensions, default "mp4, webm, ogv" when empty (comma separated)',
        required=False,
    )

    def clean(self):
        data = super(Form, self).clean()

        def split_and_strip(string):
            return [item.strip() for item in string.split(',') if item]

        data['templates'] = split_and_strip(data['templates'])
        data['extensions'] = split_and_strip(data['extensions'])
        return data

    def to_settings(self, data, settings):
        # validate aldryn settings
        if data['templates']:
            settings['DJANGOCMS_VIDEO_TEMPLATES'] = [(item, item) for item in data['templates']]
        if data['extensions']:
            settings['DJANGOCMS_VIDEO_ALLOWED_EXTENSIONS'] = data['extensions']
        return settings
