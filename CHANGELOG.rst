=========
Changelog
=========

2.0.5 (2018-10-19)
==================

* Deal with missing context from aldryn-search
* Add support for newer Django versions
* Add parameters for embed_link
* Fix swappable filer image model support


2.0.4 (2017-08-15)
==================

* Added URL parsing for the embed url. It now accepts various versions of YouTube urls and converts them to an embed link.
* Added the python3.5 test env


2.0.3 (2016-11-22)
==================

* Prevent changes to ``DJANGOCMS_VIDEO_XXX`` settings from requiring new
  migrations
* Changed naming of ``Aldryn`` to ``Divio Cloud``
* Adapted testing infrastructure (tox/travis) to incorporate
  django CMS 3.4 and dropped 3.2
* Updated translations


2.0.2 (2016-20-09)
==================

* Fixed an issues with migrations where Null values caused ``IntegrityError``


2.0.1 (2016-08-09)
==================
* Removed ``base.html`` for performance reasons
* Fixed faulty settings parsing in aldryn_config.py
* Fixed an issue where ValidationError wasn't imported
* Adapted private ``get_template`` method
* Updated translations


2.0.0 (2016-29-08)
==================

* Dropped flash support
* Dropped django CMS <3.3.1 support
* Dropped Django <1.8 support
* Renamed Video to VideoPlayer
* Added Video Source Plugin
* Added Video Track Plugin
* Adapted files to resemble best practices
* Updated translations


1.1.0 (2016-25-08)
==================

* Adapted README
* Added several config files for codecov, editorconfig and more
* Added a simple test case
* Added missing ``swfobject.min.js``
* Added missing ``player.swf``
* Added missing ``expressInstall.swf``
* Added missing ``get_flash_player-gif``
* Fixed template to include missing files


1.0.0 (2016-03-04)
==================

* Public release
