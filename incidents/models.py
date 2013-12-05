import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from urlparse import parse_qs
from mptt.fields import TreeManyToManyField


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
        verbose_name_plural = "categories"


# class IncidentCategory(Category):
#     pass

# class Feature(models.Model):
class Feature(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=200, blank=True, null=True)
    definition = models.CharField(max_length=300)
    selectable = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('incidents:features:view', kwargs={'pk': self.id})

    def __unicode__(self):
        return self.definition

    def save(self, *args, **kwargs):
        self.slug = slugify(self.definition)
        super(Feature, self).save(*args, **kwargs)

    class Meta:
        pass

    class MPTTMeta:
        order_insertion_by = ['definition']


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
        pass


class Victim(models.Model):

    UNKNOWN = '?'
    #UNKNOWN = None

    CITIZEN = 'C'
    COP = 'P'
    CATEGORY = (
        # (UNKNOWN, "Unknown"),
        (CITIZEN, "Citizen"),
        (COP, "Cop")
    )

    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        # (UNKNOWN, "Unknown"),
        (MALE, "Male"),
        (FEMALE, "Female"),
    )

    MARRIED = "M"
    SINGLE = "S"
    DIVORCED = "D"
    WIDOWED = "W"
    OTHER = "O"
    MARITAL_STATUS = (
        (UNKNOWN, "Unknown"),
        (MARRIED, "Married"),
        (SINGLE, "Single"),
        (DIVORCED, "Divorced"),
        (WIDOWED, "Widowed"),
        (OTHER, "Other")
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

    category = models.CharField(max_length=1, choices=CATEGORY, default=CITIZEN, blank=True, null=True)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDER, default=MALE, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    birthplace = models.CharField(max_length=200, blank=True, null=True)
    identity_card_number = models.CharField(max_length=20, blank=True, null=True)

    # civil_status = models.CharField(max_length=1, choices=..., default=...)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS, blank=True, null=True)
    have_children = models.NullBooleanField(blank=True, null=True)
    social_class = models.CharField(max_length=2, choices=SOCIAL_CLASS, blank=True, null=True)

    profession = models.CharField(max_length=200, blank=True, null=True)
    education = models.CharField(max_length=2, choices=EDUCATION, blank=True, null=True)

    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Victim's phone address is a private information, it wont be shared or publicly accessible.")
    email = models.EmailField(blank=True, null=True, help_text="Victim's email number is a private information, it wont be shared or publicly accessible.")

    description = models.TextField(blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('incidents:victims:view', kwargs={'pk': self.id})

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
        data.pop('email')
        data.pop('phone')
        data.pop('address')
        return data

    class Meta:
        pass


class Comment(models.Model):

    class Meta:
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
    aggressor_category = models.CharField(max_length=3, choices=CATEGORY, default=COP, blank=True)
    description = models.TextField(blank=True, null=True)
    media = models.ManyToManyField(Media, blank=True, null=True)
    sources = models.TextField(blank=True, null=True)
    features = TreeManyToManyField(Feature, blank=True, null=True)
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
        data['aggressor_category_display'] = self.get_aggressor_category_display()
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
        verbose_name_plural = "thank categories"


class ThankReport(models.Model):

    class Meta:
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
