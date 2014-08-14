djangocms-video
===============

A video plugin for django CMS.


Installation
------------

This plugin requires `django CMS` 3.0 or higher to be properly installed.

* In your projects `virtualenv`_, run ``pip install djangocms-video``.
* Add ``'djangocms_video'`` to your ``INSTALLED_APPS`` setting.
* If using Django 1.7 add ``'djangocms_video': 'djangocms_video.migrations_django',``
  to ``MIGRATION_MODULES``  (or define ``MIGRATION_MODULES`` if it does not exists);
  when django CMS 3.1 will be released, migrations for Django 1.7 will be moved
  to the standard location and the south-style ones to ``south_migrations``.
* Run ``manage.py migrate djangocms_video``.


Translations
------------

If you want to help translate the plugin please do it on transifex:

https://www.transifex.com/projects/p/django-cms/resource/djangocms-video/

