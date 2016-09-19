# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_video', '0008_reset_null_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoplayer',
            name='embed_link',
            field=models.CharField(help_text='Use this field to embed videos from external services such as YouTube, Vimeo or others. Leave it blank to upload video files by adding nested "Source" plugins.', max_length=255, verbose_name='Embed link', blank=True),
        ),
    ]
