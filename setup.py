#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from djangocms_video import __version__

REQUIREMENTS = [
    'django-cms>=3.4.5',
    'django-filer>=1.2.4',
    'djangocms-attributes-field>=0.4.0',
]


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
]


setup(
    name='djangocms-video',
    version=__version__,
    description='Adds video plugin to django CMS.',
    author='Divio AG',
    author_email='info@divio.com',
    url='https://github.com/divio/djangocms-video',
    license='BSD',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)
