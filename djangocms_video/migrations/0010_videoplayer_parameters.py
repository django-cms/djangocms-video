# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import djangocms_attributes_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_video', '0009_removed_null_values'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoplayer',
            name='parameters',
            field=djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, help_text='Parameters are appended to the video link if provided.', verbose_name='Parameters'),
        ),
    ]
