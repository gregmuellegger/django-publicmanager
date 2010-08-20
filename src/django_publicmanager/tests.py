# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.test import TestCase
from django.db import models
from django_publicmanager.managers import GenericPublicManager, PublicOnlyManager
from django_publicmanager.queryset import PublicQuerySet


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


class DefaultTestCase(TestCase):
    past_date = datetime.utcnow() - timedelta(1)
    future_date = datetime.utcnow() + timedelta(1)
    defaults = [
        [False, future_date],
        [False, past_date],
        [True, future_date],
        [True, past_date],
    ]
    def setUp(self):
        for d in self.defaults:
            PublicDefault(None, d[0], d[1]).save()
        for d in self.defaults:
            PublicNonDefault(None, d[0], d[1]).save()
        for d in self.defaults:
            IsPublic(None, d[0]).save()
        for d in self.defaults:
            PubDate(None, d[1]).save()
        for i,name in PublicStatus.STATUS_CHOICES:
            PublicStatus(None, i).save()


class TestQuerySet(DefaultTestCase):
    def test_public_method_is_public(self):
        qs = PublicQuerySet(PublicDefault,
            is_public_attr='is_public')
        self.assertEqual(
            set(PublicDefault.objects.all()),
            set(qs.all()))
        self.assertEqual(4, len(qs.all()))
        self.assertEqual(
            set(PublicDefault.objects.filter(is_public=True)),
            set(qs.public()))
        self.assertEqual(2, len(qs.public()))

    def test_public_method_pub_date(self):
        qs = PublicQuerySet(PublicDefault,
            pub_date_attr='pub_date')
        self.assertEqual(
            set(PublicDefault.objects.all()),
            set(qs.all()))
        self.assertEqual(4, len(qs.all()))
        self.assertEqual(
            set(PublicDefault.objects.filter(pub_date__lte=datetime.utcnow())),
            set(qs.public()))
        self.assertEqual(2, len(qs.public()))

    def test_public_method_both(self):
        qs = PublicQuerySet(PublicDefault,
            is_public_attr='is_public',
            pub_date_attr='pub_date')
        self.assertEqual(
            set(PublicDefault.objects.all()),
            set(qs.all()))
        self.assertEqual(4, len(qs.all()))
        self.assertEqual(
            set(PublicDefault.objects.filter(is_public=True, pub_date__lte=datetime.utcnow())),
            set(qs.public()))
        self.assertEqual(1, len(qs.public()))

    def test_public_method_status(self):
        qs = PublicQuerySet(PublicStatus,
            status_attr='status',
            status_values=PublicStatus.PUBLIC_STATUS)
        self.assertEqual(
            set(PublicStatus.objects.all()),
            set(qs.all()))
        self.assertEqual(4, len(qs.all()))
        self.assertEqual(
            set(PublicStatus.objects.filter(status__in=PublicStatus.PUBLIC_STATUS)),
            set(qs.public()))
        self.assertEqual(2, len(qs.public()))


class TestGenericPublicManager(DefaultTestCase):
    def test_default_attr_names(self):
        qs = PublicDefault.generic.all()
        self.assertEqual(
            set(PublicDefault.objects.all()),
            set(qs.all()))
        self.assertEqual(4, len(qs.all()))
        qs = PublicDefault.generic.public()
        self.assertEqual(
            set(PublicDefault.objects.filter(is_public=True, pub_date__lte=datetime.utcnow())),
            set(qs))
        self.assertEqual(1, len(qs.public()))

    def test_nondefault_attr_names(self):
        qs = PublicNonDefault.generic.all()
        self.assertEqual(
            set(PublicNonDefault.objects.all()),
            set(qs.all()))
        self.assertEqual(4, len(qs.all()))
        qs = PublicNonDefault.generic.public()
        self.assertEqual(
            set(PublicNonDefault.objects.filter(active=True, release_date__lte=datetime.utcnow())),
            set(qs))
        self.assertEqual(1, len(qs.public()))

    def test_only_is_public_attr(self):
        qs = IsPublic.generic.all()
        self.assertEqual(
            set(IsPublic.objects.all()),
            set(qs.all()))
        self.assertEqual(4, len(qs.all()))
        qs = IsPublic.generic.public()
        self.assertEqual(
            set(IsPublic.objects.filter(is_public=True)),
            set(qs))
        self.assertEqual(2, len(qs.public()))

    def test_only_pub_date_attr(self):
        qs = PubDate.generic.all()
        self.assertEqual(
            set(PubDate.objects.all()),
            set(qs.all()))
        self.assertEqual(4, len(qs.all()))
        qs = PubDate.generic.public()
        self.assertEqual(
            set(PubDate.objects.filter(pub_date__lte=datetime.utcnow())),
            set(qs))
        self.assertEqual(2, len(qs.public()))

    def test_status(self):
        qs = PublicStatus.generic.all()
        self.assertEqual(
            set(PublicStatus.objects.all()),
            set(qs))
        self.assertEqual(4, len(qs))
        qs = PublicStatus.generic.public()
        self.assertEqual(
            set(PublicStatus.objects.filter(status__in=PublicStatus.PUBLIC_STATUS)),
            set(qs))
        self.assertEqual(2, len(qs))


class TestPublicOnlyManager(DefaultTestCase):
    def test_default_attr_names(self):
        qs = PublicDefault.public.all()
        self.assertEqual(
            set(PublicDefault.objects.filter(is_public=True,
                pub_date__lte=datetime.utcnow())),
            set(qs.public()))
        self.assertEqual(1, len(qs))

    def test_nondefault_attr_names(self):
        qs = PublicNonDefault.public.all()
        self.assertEqual(
            set(PublicNonDefault.objects.filter(active=True,
                release_date__lte=datetime.utcnow())),
            set(qs))
        self.assertEqual(1, len(qs))

    def test_only_is_public_attr(self):
        qs = IsPublic.public.all()
        self.assertEqual(
            set(IsPublic.objects.filter(is_public=True)),
            set(qs))
        self.assertEqual(2, len(qs.public()))

    def test_only_pub_date_attr(self):
        qs = PubDate.public.all()
        self.assertEqual(
            set(PubDate.objects.filter(pub_date__lte=datetime.utcnow())),
            set(qs))
        self.assertEqual(2, len(qs))

    def test_status(self):
        qs = PublicStatus.public.all()
        self.assertEqual(
            set(PublicStatus.objects.filter(status__in=PublicStatus.PUBLIC_STATUS)),
            set(qs))
        self.assertEqual(2, len(qs))
