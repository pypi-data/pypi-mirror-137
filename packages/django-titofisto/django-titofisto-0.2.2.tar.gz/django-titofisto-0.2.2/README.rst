Django Time-Token File Storage
==============================

This is a simple extension to Django's `FileSystemStorage` that adds a URL
parameter carrying a shared token, which is only valid for a defined period
of time.

Functionality
-------------

This is a drop-in replacement for the Django `FileSystemStorage`, usable if
media files are served by Django itself. It does currently not work if media
files are served from an independent web server.

The storage and its accompanying view do the following:

* When a URL to a storage file is generated, a HMAC-based token is generated
* The token and the timestamp when it was generated are appended as request
  parameters to the URL
* Upon retrieval of the file through the accompanying view, the requested
  file name and the passed timestamp are used to recalculate the HMAC-based
  token
* Only if the tokens match, and a configured timeout has not passed, is the
  file served

The HMAC-based token ensures that the token is invalidated when:

* The filename changes
* The timestamp changes
* The mtime of the file changes
* The `SECRET_KEY` changes

The HMAC is salted with the `SECRET_KEY`.

Installation
------------

To add `django-titofisto`_ to a project, first add it as dependency to your
project, e.g. using `poetry`_::

  $ poetry add django-titofisto

`django-titofisto` will use the base `FileSystemStorage` for almost everything,
including determining the `MEDIA_ROOT`. It merely adds a token as URL parameter
to whatever the base `FileSystemStorage.url()` method returns.

Add the following to your settings::

  DEFAULT_FILE_STORAGE = "titofisto.TitofistoStorage"
  TITOFISTO_TIMEOUT = 3600  # optional, this is the default
  TITOFISTO_PARAM = "titofisto_token"  # optional, this is the default

Add the following to your URL config::

  from django.conf import settings
  from django.urls import include, path

  urlpatterns += [
      path(settings.MEDIA_URL.removeprefix("/"), include("titofisto.urls")),
  ]

Django will start serving media files under the configured `MEDIA_URL`.

Provide public media files
~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes, there might be media files, for example favicons,
you want to be accessible without any authentication. Per default,
`django-titofisto` will serve all files stored in the directory `public` without a token.
You can disable or configure this behavior using these settings:

  TITOFISTO_USE_PUBLIC_NAMESPACE = True # optional, this is the default
  TITOFISTO_PUBLIC_NAMESPACE = "public/" # optional, this is the default

Credits
-------

`django-titofisto` was developed for the `AlekSIS`_ school information system by
its team.

  Copyright © 2021 Dominik George <dominik.george@teckids.org>
  Copyright © 2021 Jonathan Weth <dev@jonathanweth.de>

.. _django-titofisto: https://edugit.org/AlekSIS/libs/django-titofisto
.. _poetry: https://python-poetry.org/
.. _Django's cache framework: https://docs.djangoproject.com/en/3.2/topics/cache/
.. _AlekSIS: https://aleksis.org/
