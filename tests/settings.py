#!/usr/bin/env python
# -*- coding: utf-8 -*-

HELPER_SETTINGS = {
    'INSTALLED_APPS': [
        'easy_thumbnails',
        'filer',
        'mptt',
    ],
    'LANGUAGE_CODE': 'en',
    'CMS_LANGUAGES': {
        1: [{
            'code': 'en',
            'name': 'English',
        }]
    },
    'ALLOWED_HOSTS': ['localhost'],
}


def run():
    from djangocms_helper import runner
    runner.cms('djangocms_video')


if __name__ == '__main__':
    run()
