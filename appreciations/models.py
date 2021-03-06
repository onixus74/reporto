import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import model_to_dict
from django.template.defaultfilters import slugify
from transmeta import TransMeta


class Category(models.Model):
    __metaclass__ = TransMeta

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        translate = ('definition',)

    slug = models.SlugField(_("slug"), max_length=100, blank=True, null=True)
    definition = models.CharField(_("definition"), max_length=300)

    def get_absolute_url(self):
        return reverse('appreciations:categories:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.definition

    def save(self, *args, **kwargs):
        self.slug = slugify(self.definition)
        super(Category, self).save(*args, **kwargs)


class Report(models.Model):

    class Meta:
        verbose_name = _("report")
        verbose_name_plural = _("reports")
        ordering = ['-datetime']

    datetime = models.DateTimeField(_("date and time"))
    latitude = models.FloatField(_("latitude"))
    longitude = models.FloatField(_("longitude"))
    location_text = models.CharField(_("location"), max_length=255)
    category = models.ForeignKey(Category, verbose_name=_("category"))
    subject = models.CharField(_("subject"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    media = models.ManyToManyField('base.Media', blank=True, null=True, related_name='appreciations_media+')
    # comments = models.ManyToManyField(Comment, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appreciation_created_by_user', verbose_name=_("created by"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def get_absolute_url(self):
        return reverse('appreciations:view', kwargs={'pk': self.id})

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
