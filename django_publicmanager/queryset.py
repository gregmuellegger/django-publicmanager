# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.query import QuerySet


class PublicQuerySet(QuerySet):
    is_public_attr = None
    pub_date_attr = None
    status_attr = None
    status_values = ()

    def __init__(self, model=None, query=None,
            is_public_attr=None,
            pub_date_attr=None,
            status_attr=None, status_values=(),
            *args, **kwargs):
        super(PublicQuerySet, self).__init__(model, query, *args, **kwargs)
        if is_public_attr:
            try:
                model._meta.get_field_by_name(is_public_attr)
                self.is_public_attr = is_public_attr
            except FieldDoesNotExist:
                pass
        if pub_date_attr:
            try:
                model._meta.get_field_by_name(pub_date_attr)
                self.pub_date_attr = pub_date_attr
            except FieldDoesNotExist:
                pass
        if status_attr:
            try:
                model._meta.get_field_by_name(status_attr)
                self.status_attr = status_attr
                self.status_values = status_values
            except FieldDoesNotExist:
                pass

    def public(self):
        '''
        The following conditions must be true:

            * is_public must be ``True``
            * pub_date must be ``None`` or greater/equal datetime.now()
            * status must be in ``self.status_values``
        '''
        clone = self._clone()
        if self.is_public_attr:
            clone = clone.filter(**{self.is_public_attr: True})
        if self.pub_date_attr:
            query = models.Q(**{self.pub_date_attr + '__lte': datetime.now()}) | models.Q(**{self.pub_date_attr: None})
            clone = clone.filter(query)
        if self.status_attr and self.status_values:
            clone = clone.filter(**{self.status_attr + '__in': self.status_values})
        return clone

    def _clone(self, *args, **kwargs):
        clone = super(PublicQuerySet, self)._clone(*args, **kwargs)
        for attr in (
            'is_public_attr',
            'pub_date_attr',
            'status_attr',
            'status_values'):
            setattr(clone, attr, getattr(self, attr))
        return clone
