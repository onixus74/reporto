import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import model_to_dict
from django.template.defaultfilters import slugify


logger = logging.getLogger(__name__)


class Category(models.Model):
    slug = models.SlugField(max_length=100, blank=True, null=True)
    definition = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('thanks:categories:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.definition

    def save(self, *args, **kwargs):
        self.slug = slugify(self.definition)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class Report(models.Model):

    class Meta:
        ordering = ["-datetime"]

    datetime = models.DateTimeField('date and time')
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_text = models.CharField(max_length=300)
    category = models.ForeignKey(Category)
    #subject = models.CharField()
    description = models.TextField()
    media = models.ManyToManyField('base.Media', blank=True, null=True, related_name='thanks_media+')
    # comments = models.ManyToManyField(Comment, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('thanks:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return '%s - %s %s' % (self.pk, self.datetime, self.location_text)

    def serialize(self):
        data = model_to_dict(self)
        data['created_by'] = self.created_by
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['category'] = self.category
        data['media'] = self.media.all()
        # data['comments'] = self.comments.all()
        return data


import watson

watson.register(Report)
