import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import model_to_dict
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from mptt.fields import TreeManyToManyField
from mptt.models import MPTTModel, TreeForeignKey


class Category(models.Model):

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    slug = models.SlugField(_("slug"), max_length=100, blank=True, null=True)
    definition = models.CharField(_("definition"), max_length=300)

    def get_absolute_url(self):
        return reverse('violations:categories:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.definition

    def save(self, *args, **kwargs):
        self.slug = slugify(self.definition)
        super(Category, self).save(*args, **kwargs)


# class Feature(models.Model):
class Feature(MPTTModel):

    class Meta:
        verbose_name = _("feature")
        verbose_name_plural = _("features")

    parent = TreeForeignKey('self', related_name='children', verbose_name=_("children features"), null=True, blank=True)
    slug = models.SlugField(_("slug"), max_length=200, blank=True, null=True)
    definition = models.CharField(_("definition"), max_length=300)
    selectable = models.BooleanField(_("is selectable?"), default=True)

    def get_absolute_url(self):
        return reverse('violations:features:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.definition

    def save(self, *args, **kwargs):
        self.slug = slugify(self.definition)
        super(Feature, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['definition']


class Victim(models.Model):

    class Meta:
        verbose_name = _("victim")
        verbose_name_plural = _("victims")

    UNKNOWN = '?'
    #UNKNOWN = None

    CITIZEN = 'C'
    COP = 'P'
    CATEGORY = (
        # (UNKNOWN, _("Unknown"),
        (CITIZEN, _("Citizen")),
        (COP, _("Cop"))
    )

    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        # (UNKNOWN, _("Unknown")),
        (MALE, _("Male")),
        (FEMALE, _("Female")),
    )

    MARRIED = 'M'
    SINGLE = 'S'
    DIVORCED = 'D'
    WIDOWED = 'W'
    OTHER = 'O'
    MARITAL_STATUS = (
        (UNKNOWN, _("Unknown")),
        (MARRIED, _("Married")),
        (SINGLE, _("Single")),
        (DIVORCED, _("Divorced")),
        (WIDOWED, _("Widowed")),
        (OTHER, _("Other"))
    )

    LOWER = 'L'
    MIDDLE = 'M'
    UPPER = 'U'
    SOCIAL_CLASS = (
        (UNKNOWN, _("Unknown")),
        (LOWER, _("Lower")),
        (MIDDLE, _("Middle")),
        (UPPER, _("Upper"))
    )

    NO_EDUCATION = 'NO'
    PRIMARY_SCHOOL = 'PS'
    HIGH_SCHOOL = 'HS'
    UNIVERSITY = 'UN'
    EDUCATION = (
        (UNKNOWN, _("Unknown")),
        (NO_EDUCATION, _("No Education")),
        (PRIMARY_SCHOOL, _("Primary School")),
        (HIGH_SCHOOL, _("High School")),
        (UNIVERSITY, _("University"))
    )

    category = models.CharField(_("category"), max_length=1, choices=CATEGORY, default=CITIZEN, blank=True, null=True)
    firstname = models.CharField(_("first name"), max_length=100, blank=True, null=True)
    lastname = models.CharField(_("last name"), max_length=100, blank=True, null=True)

    gender = models.CharField(_("gender"), max_length=1, choices=GENDER, default=MALE, blank=True, null=True)
    birthdate = models.DateField(_("birth date"), blank=True, null=True)
    birthplace = models.CharField(_("birth place"), max_length=200, blank=True, null=True)
    identity_card_number = models.CharField(_("identity card number"), max_length=20, blank=True, null=True, help_text=_("Private information."))

    # civil_status = models.CharField(max_length=1, choices=..., default=...)
    marital_status = models.CharField(_("marital status"), max_length=1, choices=MARITAL_STATUS, blank=True, null=True)
    have_children = models.NullBooleanField(_("have children?"), blank=True, null=True)
    social_class = models.CharField(_("social class"), max_length=2, choices=SOCIAL_CLASS, blank=True, null=True)

    education = models.CharField(_("education"), max_length=2, choices=EDUCATION, blank=True, null=True)
    profession = models.CharField(_("profession"), max_length=200, blank=True, null=True)

    address = models.TextField(_("address"), null=True, blank=True)
    phone = models.CharField(_("phone"), max_length=20, blank=True, null=True, help_text=_("Private information."))
    email = models.EmailField(_("email"), blank=True, null=True, help_text=_("Private information."))

    description = models.TextField(_("description"), blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), blank=True, null=True)

    def get_absolute_url(self):
        return reverse('violations:victims:view', kwargs={'pk': self.id})

    def get_fullname(self):
        return "%s %s" % (self.firstname, self.lastname)

    def __unicode__(self):
        return self.get_fullname()

    def serialize(self):
        data = model_to_dict(self)
        data['category_display'] = self.get_category_display()
        data['marital_status_display'] = self.get_marital_status_display()
        data['gender_display'] = self.get_gender_display()

        data['education_display'] = self.get_education_display()
        data['user'] = self.user

        data.pop('address')
        data.pop('phone')
        data.pop('email')

        data.pop('identity_card_number')
        return data


class Comment(models.Model):

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
        ordering = ['created_at']

    UPDATE = 'U'
    CORRECTION = 'C'
    TYPE = (
        (UPDATE, _("Update")),
        (CORRECTION, _("Correction")),
    )
    type = models.CharField(_("type"), max_length=1, choices=TYPE, default=UPDATE)
    content = models.TextField(_("content"), null=True, blank=True)
    attachment = models.FileField(_("attachment"), upload_to='reports/comments/', null=True, blank=True)
    # report     = models.ForeignKey(Report, verbose_name=_("report"))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("created by"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __unicode__(self):
        return "%s %s %s" % (self.created_at, self.type, self.content)

    def clean(self):
        # logger.debug('MODEL Comment clean %s', [self.content, self.content is None, self.attachment, self.attachment is None])
        if not self.content and not self.attachment:
            raise ValidationError("Comment content and attachment can not be both empty.")

    def serialize(self):
        data = model_to_dict(self)
        data['type_display'] = self.get_type_display()
        data['attachment'] = self.attachment.url if self.attachment else None
        data['created_by'] = self.created_by
        data['created_at'] = self.created_at
        return data

    def save(self, *args, **kwargs):
        self.content = strip_tags(self.content)
        super(Comment, self).save(*args, **kwargs)


class Report(models.Model):

    class Meta:
        verbose_name = _("report")
        verbose_name_plural = _("reports")
        ordering = ['-datetime']

    CITIZEN = 'CIT'
    COP = 'COP'
    CATEGORY = (
        (CITIZEN, _("Citizen")),
        (COP, _("Cop")),
    )

    datetime = models.DateTimeField(_("date and time"),)
    latitude = models.FloatField(_("latitude"))
    longitude = models.FloatField(_("longitude"))
    location_text = models.CharField(_("location"), max_length=300)
    category = models.ForeignKey(Category, verbose_name=_("category"))
    victim = models.ForeignKey(Victim, verbose_name=_("victim"))
    aggressor = models.TextField(_("aggressor"), blank=True, null=True)
    aggressor_category = models.CharField(_("aggressor category"), max_length=3, choices=CATEGORY, default=COP, blank=True)
    description = models.TextField(_("description"), blank=True, null=True)
    media = models.ManyToManyField('base.Media', blank=True, null=True, related_name='violations_media+')
    sources = models.TextField(_("sources"), blank=True, null=True)
    features = TreeManyToManyField(Feature, blank=True, null=True)
    is_verified = models.BooleanField(_("is verified?"))
    # verified_by = models.ManyToManyField('auth.Group', blank=True, null=True)
    is_closed = models.BooleanField(_("is closed?"))
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='violation_created_by_user', verbose_name=_("created by"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    def get_absolute_url(self):
        return reverse('violations:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return '%s - %s %s' % (self.pk, self.datetime, self.location_text)

    def serialize(self):
        data = model_to_dict(self)
        data['created_by'] = self.created_by
        data['created_at'] = self.created_at
        data['updated_at'] = self.updated_at
        data['category'] = self.category
        data['features'] = self.features.all()
        data['victim'] = self.victim
        data['media'] = self.media.all()
        data['comments'] = self.comments.all()
        data['aggressor_category_display'] = self.get_aggressor_category_display()
        return data


import watson

watson.register(Report)
