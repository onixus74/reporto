import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from urlparse import parse_qs


class Category(models.Model):
    slug = models.SlugField(max_length=100, blank=True, null=True)
    definition = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('incidents:categories:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.definition

    def save(self, *args, **kwargs):
        self.slug = slugify(self.definition)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        db_table = 'reports_category'
        verbose_name_plural = "categories"


# class IncidentCategory(Category):
#     pass


class Feature(models.Model):
    slug = models.SlugField(max_length=200, blank=True, null=True)
    definition = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('incidents:features:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.definition

    def save(self, *args, **kwargs):
        self.slug = slugify(self.definition)
        super(Feature, self).save(*args, **kwargs)

    class Meta:
        db_table = 'reports_feature'


class Media(models.Model):
    IMAGE = 'I'
    VIDEO = 'V'
    TYPE = (
        (IMAGE, "Image"),
        (VIDEO, "Video"),
    )
    # title        = models.CharField(max, blank=True, null=True_length=200)
    # description  = models.TextField()
    url = models.URLField(max_length=300)
    file = models.FileField(upload_to='reports/', blank=True, null=True)
    # video_thumbnail = models.ImageField(upload_to='reports/', blank=True, null=True)
    # external = models.BooleanField()

    def __unicode__(self):
        # return self.file.url
        return self.url

    # def clean(self):
    # 	if not self.url:
    # 		raise ValidationError('URL can not be empty.')

    def save(self, *args, **kwargs):
        if self.file:
            self.url = self.file.url
        # else:
        # 	self.external = True
        super(Media, self).save(*args, **kwargs)
        # if self.file:
        # 	self.url = self.file.url
        # 	super(Media, self).save(*args, **kwargs)

    def get_url(self):
        return self.url or self.file.url

    def is_file(self):
        return self.file

    def is_youtube(self):
        return self.url.find('youtube.com') >= 0

    def get_youtube_thumbnail(self):
        qs = self.url.split('?')
        video_id = parse_qs(qs[1])['v'][0]
        return "http://img.youtube.com/vi/%s/1.jpg" % video_id

    def serialize(self):
        data = model_to_dict(self)
        # data['file'] = { 'url': self.url }
        data.pop('file')
        data['url'] = self.url
        return data

    class Meta:
        db_table = 'reports_media'


class Victim(models.Model):

    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    CITIZEN = 'CIT'
    COP = 'COP'
    CATEGORY = (
        (CITIZEN, "Citizen"),
        (COP, "Cop")
    )

    UNKNOWN = '?'

    NO_EDUCATION = 'NO'
    PRIMARY_SCHOOL = 'PS'
    HIGH_SCHOOL = 'HS'
    UNIVERSITY = 'UN'
    EDUCATION = (
        (UNKNOWN, "Unknown"),
        (NO_EDUCATION, "No Education"),
        (PRIMARY_SCHOOL, "Primary School"),
        (HIGH_SCHOOL, "High School"),
        (UNIVERSITY, "University")
    )

    LOWER = 'L'
    MIDDLE = 'M'
    UPPER = 'U'
    SOCIAL_CLASS = (
        (UNKNOWN, "Unknown"),
        (LOWER, "Lower"),
        (MIDDLE, "Middle"),
        (UPPER, "Upper")
    )

    category = models.CharField(
        max_length=3, choices=CATEGORY, default=CITIZEN)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER, default=MALE)
    age = models.PositiveIntegerField(blank=True, null=True)
    education = models.CharField(
        max_length=2, choices=EDUCATION, default=UNKNOWN)
    social_class = models.CharField(
        max_length=2, choices=SOCIAL_CLASS, default=UNKNOWN)
    profession = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True,
                             help_text="Victim's phone address is a private information, it wont be shared or publicly accessible.")
    email = models.EmailField(
        blank=True, null=True, help_text="Victim's email number is a private information, it wont be shared or publicly accessible.")
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('incidents:victims:view', kwargs={'pk': self.id})

    def get_fullname(self):
        return "%s %s" % (self.firstname, self.lastname)

    def __unicode__(self):
        return self.get_fullname()

    def serialize(self):
        data = model_to_dict(self)
        data['gender_display'] = self.get_gender_display()
        data['category_display'] = self.get_category_display()
        data['education_display'] = self.get_education_display()
        data['user'] = self.user
        data.pop('email')
        data.pop('phone')
        return data

    class Meta:
        db_table = 'reports_victim'


class Comment(models.Model):


    class Meta:
        db_table = 'reports_comment'
        ordering = ["created_at"]

    UPDATE = 'U'
    CORRECTION = 'C'
    TYPE = (
        (UPDATE, "Update"),
        (CORRECTION, "Correction"),
    )
    type = models.CharField(max_length=1, choices=TYPE, default=UPDATE)
    content = models.TextField(null=True, blank=True)
    attachment = models.FileField(
        upload_to='reports/comments/', null=True, blank=True)
    # report     = models.ForeignKey(Report)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content

    def clean(self):
        # logger.debug('MODEL Comment clean %s', [self.content, self.content is None, self.attachment, self.attachment is None])
        if not self.content and not self.attachment:
            raise ValidationError(
                'Comment content and attachment can not be both empty.')

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
        db_table = 'reports_report'
        ordering = ["-datetime"]

    CITIZEN = 'CIT'
    COP = 'COP'
    CATEGORY = (
        (CITIZEN, "Citizen"),
        (COP, "Cop"),
    )

    datetime = models.DateTimeField('date and time')
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_text = models.CharField(max_length=300)
    category = models.ForeignKey(Category)
    victim = models.ForeignKey(Victim)
    aggressor = models.TextField(blank=True, null=True)
    aggressor_category = models.CharField(
        max_length=3, choices=CATEGORY, default=COP, blank=True)
    description = models.TextField()
    media = models.ManyToManyField(Media, blank=True, null=True)
    sources = models.TextField(blank=True, null=True)
    features = models.ManyToManyField(Feature)
    is_verified = models.BooleanField()
    is_closed = models.BooleanField()
    comments = models.ManyToManyField(Comment, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('incidents:view', kwargs={'pk': self.id})

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
        data[
            'aggressor_category_display'] = self.get_aggressor_category_display()
        return data




class ThankCategory(models.Model):
    slug = models.SlugField(max_length=100, blank=True, null=True)
    definition = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('thanks:categories:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.definition

    def save(self, *args, **kwargs):
        self.slug = slugify(self.definition)
        super(ThankCategory, self).save(*args, **kwargs)

    class Meta:
        db_table = 'reports_thankcategory'
        verbose_name_plural = "thank categories"


class ThankReport(models.Model):

    class Meta:
        db_table = 'reports_thankreport'
        ordering = ["-datetime"]

    datetime = models.DateTimeField('date and time')
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_text = models.CharField(max_length=300)
    category = models.ForeignKey(ThankCategory)
    #subject = models.CharField()
    description = models.TextField()
    media = models.ManyToManyField(Media, blank=True, null=True)
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
