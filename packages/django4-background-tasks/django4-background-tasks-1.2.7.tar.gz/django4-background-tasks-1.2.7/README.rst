=========================
Django 4 Background Tasks
=========================

.. note::
   This is an adaptation of django-background-tasks that removes django-compat and makes other small changes to allow compatilibity with Django 4.0.

   It is also compatible with Django 3 (at least).

.. image:: https://readthedocs.org/projects/django4-background-tasks/badge/?version=latest
    :target: http://django4-background-tasks.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/django4-background-tasks.svg
    :target: https://pypi.python.org/pypi/django4-background-tasks
    :alt: PyPI

Django Background Task is a database-backed work queue for Django, loosely based around `Ruby's DelayedJob`_ library. This project was adopted and adapted from lilspikey_ `django-background-task`.

.. _Ruby's DelayedJob: https://github.com/tobi/delayed_job
.. _lilspikey: https://github.com/lilspikey/

To avoid conflicts on PyPI we renamed it to django-background-tasks (plural). For an easy upgrade from django-background-task to django-background-tasks, the internal module structure were left untouched.

In Django Background Task, all tasks are implemented as functions (or any other callable).

There are two parts to using background tasks:

- creating the task functions and registering them with the scheduler
- setup a cron task (or long running process) to execute the tasks


Docs
====
See `Read the docs`_.

.. _Read the docs: http://django-background-tasks.readthedocs.io/en/latest/
