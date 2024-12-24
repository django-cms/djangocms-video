================
django CMS Video
================

|pypi| |build| |coverage|

**django CMS Video** is a set of plugins for `django CMS <http://django-cms.org>`_
that allow you to publish video content on your site (using an HTML5 player by default,
but you can override this in your own templates if required).

It uses files managed by `Django Filer <https://github.com/divio/django-filer>`_.

.. note:: 
        
        This project is endorsed by the `django CMS Association <https://www.django-cms.org/en/about-us/>`_.
        That means that it is officially accepted by the dCA as being in line with our roadmap vision and development/plugin policy. 
        Join us on `Slack <https://www.django-cms.org/slack/>`_.

.. image:: preview.gif


*******************************************
Contribute to this project and win rewards
*******************************************

Because this is a an open-source project, we welcome everyone to
`get involved in the project <https://www.django-cms.org/en/contribute/>`_ and
`receive a reward <https://www.django-cms.org/en/bounty-program/>`_ for their contribution. 
Become part of a fantastic community and help us make django CMS the best CMS in the world.   

We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/django-cms/djangocms-video/graphs/contributors>`_
section.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/djangocms-video/blob/master/setup.py>`_
file for additional dependencies:

|python| |django| |djangocms|

* Django Filer 1.7 or higher

Make sure `django-filer <http://django-filer.readthedocs.io/en/latest/installation.html>`_
is installed and configured appropriately.


Installation
------------

For a manual install:

* run ``pip install djangocms-video``
* add ``djangocms_video`` to your ``INSTALLED_APPS``
* run ``python manage.py migrate djangocms_video``


Configuration
-------------

Note that the provided templates are very minimal by design. You are encouraged
to adapt and override them to your project's requirements.

This addon provides a ``default`` template for all instances. You can provide
additional template choices by adding a ``DJANGOCMS_VIDEO_TEMPLATES``
setting::

    from django.utils.translation import gettext_lazy as _

    DJANGOCMS_VIDEO_TEMPLATES = [
        ('feature', _('Featured Version')),
    ]

You'll need to create the `feature` folder inside ``templates/djangocms_video/``
otherwise you will get a *template does not exist* error. You can do this by
copying the ``default`` folder inside that directory and renaming it to
``feature``.

``MP4``, ``WEBM`` and ``OGV`` files are allowed by default. We recommend
adding all 3 source files for full browser compatibility. You can change
the default setting by overriding::

    DJANGOCMS_VIDEO_ALLOWED_EXTENSIONS = ['mp4', 'webm', 'ogv']

The plugin detects YouTube URLs using a regular expression and canonicalizes
them to `//www.youtube.com/embed/{}` where the placeholder is replaced by the
video id.

The canonical URL can be reconfigured with a configuration setting::

    DJANGOCMS_VIDEO_YOUTUBE_EMBED_URL = '//www.youtube-nocookie.com/embed/{}'

In addition to regular video files and YouTube videos, the plugin also supports `HLS <https://en.wikipedia.org/wiki/HTTP_Live_Streaming>`_ or HTTP Live Streams as source. These streams are played back using an html <video> element with the added support of `hls.js <https://hlsjs.video-dev.org>`_. An HLS source is defined by an URL pointing to a .m3u8 file served via HTTP.

By default the HLS source includes the hls.js javascript file from a content delivery network. If you wish to override this, customize the following variable::

   DJANGOCMS_VIDEO_HLSJS_SOURCE = 'https://cdn.jsdelivr.net/npm/hls.js@1.5.17/dist/hls.min.js'

Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test


.. |pypi| image:: https://badge.fury.io/py/djangocms-video.svg
    :target: http://badge.fury.io/py/djangocms-video
.. |build| image:: https://travis-ci.org/divio/djangocms-video.svg?branch=master
    :target: https://travis-ci.org/divio/djangocms-video
.. |coverage| image:: https://codecov.io/gh/divio/djangocms-video/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/divio/djangocms-video

.. |python| image:: https://img.shields.io/badge/python-3.5+-blue.svg
    :target: https://pypi.org/project/djangocms-video/
.. |django| image:: https://img.shields.io/badge/django-2.2,%203.0,%203.1-blue.svg
    :target: https://www.djangoproject.com/
.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.7%2B-blue.svg
    :target: https://www.django-cms.org/
