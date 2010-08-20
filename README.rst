====================
django-publicmanager
====================

The django-publicmanager application provides a custom queryset class and
managers that handle the public availability of database objects. The classes
provide a ``public`` method that filters by boolean ``is_public`` and date
based ``pub_date`` fields.

Installation
============

All you need to install the django-publicmanager package is a simple ``sudo
easy_install dango-publicmanager``.

Usage
=====

The package contains just two managers. The manager ``GenericPublicManager``
works exactly like django's default manager except that it provides a
``public()`` method that returns only public available objects. The athor
manager, ``PublicOnlyManager``, returns public objects by default without
calling any extra method.

It should be obvious that you will at least need a model to use one or both of these
managers. The managers will use one or more of the following fields to
determine if an object is public or not.

* ``is_public``: This must be a ``models.BooleanField`` and if it is set to
  ``True``, it will be treated as public.

* ``pub_date`` must be a ``models.DateTimeField`` or ``models.DateField``. The
  date must be either in the past or equal to the current time to make the
  object public.

* You can use a status field which holds information about the public
  availability of the object. To use it you must provide the ``status_attr``
  and ``status_values`` attributes to the manager. The ``status_attr``
  specifies the field name. If the field's value is found in list
  ``status_values`` the object will be public. The most common use of this
  feature is to use it with choices. See the examples below.


An object is only public if all of these fields, if existent in the model, are
evaluated to be public. This means if ``is_public`` is set to ``True`` but
``pub_date`` points to a date in the future the whole objects will be treated
as not public.

Examples
========

Here is a pretty simple example using only the ``is_public`` and ``pub_date``
fields::

    from django.db import models
    from django_publicmanager.managers import GenericPublicManager, PublicOnlyManager

    class Example(models.Model):
        title = models.CharField(max_length=50)
        is_public = models.BooleanField(default=True)
        pub_date = models.DateTimeField()

        objects = GenericPublicManager()
        public = PublicOnlyManager()

Now you can access the objects like this::

    >>> Example.objects.create(title='A', is_public=True, pub_date=datetime.now())
    >>> Example.objects.create(title='B', is_public=True, pub_date=datetime.now() + timedelta(1))
    >>> Example.objects.create(title='C', is_public=False, pub_date=datetime.now())
    >>> Example.objects.create(title='D', is_public=True, pub_date=datetime.now() - timedelta(1))
    >>> Example.objects.all()
    [<Example: A>, <Example: B>, <Example: C>, <Example: D>]
    >>> Example.objects.public()
    [<Example: A>, <Example: D>]
    >>> Example.public.all()
    [<Example: A>, <Example: D>]
    >>> Example.objects.public()
    [<Example: A>, <Example: D>]
    >>> Example.objects.filter(title='A').public()
    [<Example: A>]

You don't have to name the fields exactly like above. But if you use athor
names, you have to tell the managers the new names::

    from django.db import models
    from django_publicmanager.managers import GenericPublicManager, PublicOnlyManager

    class Example(models.Model):
        title = models.CharField(max_length=50)
        online = models.BooleanField(default=True)
        available_from = models.DateTimeField()

        objects = GenericPublicManager(
            is_public_attr='online',
            pub_date_attr='available_from')
        public = PublicOnlyManager(
            is_public_attr='online',
            pub_date_attr='available_from')

Last but not least, an example with the ``status`` field::

    from django.db import models
    from django_publicmanager.managers import GenericPublicManager, PublicOnlyManager

    class Example(models.Model):
        STATUS_CHOICES = (
            (1, 'draft'),
            (2, 'review'),
            (3, 'public'),
            (4, 'featured'),
        )

        title = models.CharField(max_length=50)
        status = models.PositiveIntegerField(choices=STATUS_CHOICES)

        objects = GenericPublicManager(
            status_attr='status',
            status_values=(3,4))
        public = PublicOnlyManager(
            status_attr='status',
            status_values=(3,4))
