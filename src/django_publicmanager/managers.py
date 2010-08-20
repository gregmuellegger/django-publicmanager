# -*- coding: utf-8 -*-
from django.db import models
from django_publicmanager.queryset import PublicQuerySet


class GenericPublicManager(models.Manager):
    '''
    This manager returns a ``PublicQuerySet``. At default it returns all
    objects not only public objects. Call ``public()`` on the manager or on the
    ``PublicQuerySet`` to retrieve only public objects.

    It uses two different fields on a model to determine if its public or not.
    If ``is_public`` is set to ``True`` and ``pub_date`` is less than the
    current date the object is handled as public. 
    '''
    # TODO: write more documentation
    def __init__(self,
            is_public_attr='is_public',
            pub_date_attr='pub_date',
            status_attr=None, status_values=None,
            *args, **kwargs):
        self.is_public_attr = is_public_attr
        self.pub_date_attr = pub_date_attr
        self.status_attr = status_attr
        self.status_values = status_values
        super(GenericPublicManager, self).__init__(*args, **kwargs)

    def get_query_set(self, *args, **kwargs):
        return PublicQuerySet(self.model,
            is_public_attr=self.is_public_attr,
            pub_date_attr=self.pub_date_attr,
            status_attr=self.status_attr,
            status_values=self.status_values,
            *args, **kwargs)

    def public(self, *args, **kwargs):
        return self.get_query_set().public(*args, **kwargs)


class PublicOnlyManager(GenericPublicManager):
    '''
    Subclass of ``GenericPublicManager``. It returns only public objects.
    '''
    def get_query_set(self, *args, **kwargs):
        return super(PublicOnlyManager, self).get_query_set().public(*args, **kwargs)
