# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django_publicmanager.managers import GenericPublicManager, PublicOnlyManager


class PublicDefault(models.Model):
    is_public = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=datetime.utcnow)

    objects = models.Manager()
    generic = GenericPublicManager()
    public = PublicOnlyManager()

    def __unicode__(self):
        return unicode(self.pk)


class PublicNonDefault(models.Model):
    active = models.BooleanField(default=True)
    release_date = models.DateField(default=datetime.utcnow)

    objects = models.Manager()
    generic = GenericPublicManager(
        is_public_attr='active',
        pub_date_attr='release_date')
    public = PublicOnlyManager(
        is_public_attr='active',
        pub_date_attr='release_date')

    def __unicode__(self):
        return unicode(self.pk)


class IsPublic(models.Model):
    is_public = models.BooleanField(default=True)

    objects = models.Manager()
    generic = GenericPublicManager()
    public = PublicOnlyManager()

    def __unicode__(self):
        return unicode(self.pk)


class PubDate(models.Model):
    pub_date = models.DateTimeField(default=datetime.utcnow)

    objects = models.Manager()
    generic = GenericPublicManager()
    public = PublicOnlyManager()

    def __unicode__(self):
        return unicode(self.pk)


class PublicStatus(models.Model):
    STATUS_DRAFT = 1
    STATUS_PUBLIC = 2
    STATUS_FEATURED = 3
    STATUS_ARCHIVE = 4
    STATUS_CHOICES = (
        (STATUS_DRAFT, 'draft'),
        (STATUS_PUBLIC, 'public'),
        (STATUS_FEATURED, 'featured'),
        (STATUS_ARCHIVE, 'archivied'),
    )
    PUBLIC_STATUS = (2,3)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES)

    objects = models.Manager()
    generic = GenericPublicManager(status_attr='status',
        status_values=(STATUS_PUBLIC, STATUS_FEATURED))
    public = PublicOnlyManager(status_attr='status',
        status_values=(STATUS_PUBLIC, STATUS_FEATURED))

    def __unicode__(self):
        return unicode(self.pk)
