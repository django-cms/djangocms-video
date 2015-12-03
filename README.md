djangocms-video
===============

A video plugin for django CMS.


Installation
------------

This plugin requires `django CMS` 3.0 or higher to be properly installed.

* In your projects `virtualenv`, run ``pip install djangocms-video``.
* Add ``'djangocms_video'`` to your ``INSTALLED_APPS`` setting.
* If using Django 1.6 and South < 1.0.2 add ``'djangocms_video': 'djangocms_video.migrations_django',``
  to ``SOUTH_MIGRATION_MODULES``  (or define ``SOUTH_MIGRATION_MODULES`` if it
  does not exist).
* Run ``manage.py migrate djangocms_video``.


Translations
------------

If you want to help translate the plugin please do it on transifex:

https://www.transifex.com/projects/p/django-cms/resource/djangocms-video/

