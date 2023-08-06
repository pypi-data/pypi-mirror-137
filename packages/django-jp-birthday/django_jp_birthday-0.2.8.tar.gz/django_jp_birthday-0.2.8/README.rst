django-jp-birthday
==================

|https://pypi.python.org/pypi/django_jp_birthday| |image|
|https://img.shields.io:/pypi/djversions/django-jp-birthday|
|https://django-jp-birthday.readthedocs.io/en/latest/?version=latest|
|Updates| |Python 3|
|https://img.shields.io/github/repo-size/shimakaze-git/django-jp-birthday|
|https://img.shields.io/github/languages/code-size/shimakaze-git/django-jp-birthday|
|https://codecov.io/gh/shimakaze-git/django-jp-birthday/branch/master/graph/badge.svg|
|https://img.shields.io/github/license/shimakaze-git/django-jp-birthday.svg|
|image| |.github/workflows/test.yml|

django-jp-birthday is a django’s model for use Japanese birthdays and
ages.

Based library is https://github.com/bashu/django-birthday .

Authored by `shimakaze_soft <https://github.com/shimakaze-git>`__ and
some great

`contributors <https://github.com/shimakaze-git/django-jp-birthday/CONTRIBUTING.rst>`__

Features
========

-  Get all user profiles within the next 30 days
-  Get all user profiles which have their birthday today
-  order the user profiles according to their birthday

-  Converting Birthdays to Japanese Style
-  Calculate age based on birthday
-  Get all birthdays in the specified Japanese calendar

Installation
============

-  `pypi <https://pypi.org/project/django-jp-birthday/>`__

.. code:: bash

   $ pip install django-jp-birthday

   $ python steup.py install

Usage
=====

django-jp-birthday provides a ``jp_birthday.models.BirthdayModel`` model
type which is a subclass of django.db.models.Model and thus has the same
characteristics as that.

``jp_birthday.managers.JpBirthdayManager`` is used as a manager for
``jp_birthday.models.BirthdayModel`` and provides various methods.

.. code:: python

   from jp_birthday.models import BirthdayModel

   class ModelsTest(BirthdayModel):

       class Meta:
           app_label = 'jp_birthday'
           ordering = ('pk',)

Get all user profiles within the next 30 days:

.. code:: python

   ModelsTest.objects.get_upcoming_birthdays()

Get all user profiles which have their birthday today:

.. code:: python

   ModelsTest.objects.get_birthdays()

Or order the user profiles according to their birthday:

.. code:: python

   ModelsTest.objects.order_by_birthday()

Docs
====

-  Documentation: https://django-jp-birthday.readthedocs.io.

License
=======

``django-jp-birthday`` is released under the MIT license.

.. |https://pypi.python.org/pypi/django_jp_birthday| image:: https://img.shields.io/pypi/v/django_jp_birthday.svg
.. |image| image:: https://img.shields.io/pypi/pyversions/django-jp-birthday.svg
   :target: https://pypi.org/project/django-jp-birthday
.. |https://img.shields.io:/pypi/djversions/django-jp-birthday| image:: https://img.shields.io:/pypi/djversions/django-jp-birthday
.. |https://django-jp-birthday.readthedocs.io/en/latest/?version=latest| image:: https://readthedocs.org/projects/django-jp-birthday/badge/?version=latest
.. |Updates| image:: https://pyup.io/repos/github/shimakaze-git/django-jp-birthday/shield.svg
   :target: https://pyup.io/repos/github/shimakaze-git/django-jp-birthday/
.. |Python 3| image:: https://pyup.io/repos/github/shimakaze-git/django-jp-birthday/python-3-shield.svg
   :target: https://pyup.io/repos/github/shimakaze-git/django-jp-birthday/
.. |https://img.shields.io/github/repo-size/shimakaze-git/django-jp-birthday| image:: https://img.shields.io/github/repo-size/shimakaze-git/django-jp-birthday
.. |https://img.shields.io/github/languages/code-size/shimakaze-git/django-jp-birthday| image:: https://img.shields.io/github/languages/code-size/shimakaze-git/django-jp-birthday
.. |https://codecov.io/gh/shimakaze-git/django-jp-birthday/branch/master/graph/badge.svg| image:: https://codecov.io/gh/shimakaze-git/django-jp-birthday/branch/master/graph/badge.svg
.. |https://img.shields.io/github/license/shimakaze-git/django-jp-birthday.svg| image:: https://img.shields.io/github/license/shimakaze-git/django-jp-birthday.svg
.. |image| image:: https://img.shields.io/pypi/dm/django-jp-birthday
   :target: https://img.shields.io/pypi/dm/django-jp-birthday
.. |.github/workflows/test.yml| image:: https://github.com/shimakaze-git/django-jp-birthday/actions/workflows/test.yml/badge.svg
   :target: https://github.com/shimakaze-git/django-jp-birthday/actions/workflows/test.yml
