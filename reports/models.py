import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.forms.models import model_to_dict


class Category(models.Model):
	slug       = models.SlugField(max_length=100, blank=True, null=True)
	definition = models.CharField(max_length=300)

	def get_absolute_url(self):
		return reverse('categories:view', args=[str(self.id)])

	def __unicode__(self):
		return self.definition

	def save(self, *args, **kwargs):
		self.slug = slugify(self.definition)
		super(Category, self).save(*args, **kwargs)


class Feature(models.Model):
	slug       = models.SlugField(max_length=200, blank=True, null=True)
	definition = models.CharField(max_length=300)

	def get_absolute_url(self):
		return reverse('features:view', args=[str(self.id)])

	def __unicode__(self):
		return self.definition

	def save(self, *args, **kwargs):
		self.slug = slugify(self.definition)
		super(Feature, self).save(*args, **kwargs)


class Media(models.Model):

	#title        = models.CharField(max_length=200)
	#description  = models.TextField()
	#url  = models.URLField(max_length=300)
	file = models.FileField(upload_to='reports/')

	def __unicode__(self):
		return self.file.url

	# def save(self, *args, **kwargs):
	# 	if self.file:
	# 		self.url = self.file.url
	# 	super(Media, self).save(*args, **kwargs)

	# def get_url(self):
	# 	return self.url or self.file.url

	def serialize(self):
		data = model_to_dict(self)
		data['file'] = { 'url': self.file.url }
		return data


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

	firstname   = models.CharField(max_length=100)
	lastname    = models.CharField(max_length=100)
	gender      = models.CharField(max_length=1, choices=GENDER, default=MALE)
	age         = models.PositiveIntegerField()
	education   = models.CharField(max_length=200)
	profession  = models.CharField(max_length=200)
	phone       = models.CharField(max_length=20)
	email       = models.EmailField()
	description = models.TextField()
	category    = models.CharField(max_length=3, choices=CATEGORY, default=CITIZEN, blank=True)
	user        = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

	def get_absolute_url(self):
		return reverse('victims:view', args=[str(self.id)])

	def __unicode__(self):
		return self.firstname + " " + self.lastname

	def serialize(self):
		data = model_to_dict(self)
		data['gender_display'] = self.get_gender_display()
		data['category_display'] = self.get_category_display()
		data['user'] = self.user
		return data


class Comment(models.Model):

	class Meta:
		ordering = ["created_at"]

	UPDATE = 'U'
	CORRECTION = 'C'
	TYPE = (
		(UPDATE, "Update"),
		(CORRECTION, "Correction"),
	)
	type       = models.CharField(max_length=1, choices=TYPE, default=UPDATE)
	content    = models.TextField()
	file       = models.FileField(upload_to='reports/comments/', null=True, blank=True)
	#report     = models.ForeignKey(Report)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.content

	def serialize(self):
		data = model_to_dict(self)
		data['type_display'] = self.get_type_display()
		data['file'] = self.file.url if self.file else None
		data['created_by'] = self.created_by
		data['created_at'] = self.created_at
		return data

	def save(self, *args, **kwargs):
		self.content = strip_tags(self.content)
		super(Comment, self).save(*args, **kwargs)


class Report(models.Model):

	class Meta:
		ordering = ["datetime"]

	CITIZEN = 'CIT'
	COP = 'COP'
	CATEGORY = (
		(CITIZEN, "Citizen"),
		(COP, "Cop"),
	)

	datetime           = models.DateTimeField('date and time')
	location           = models.CharField(max_length=100)
	location_text      = models.CharField(max_length=300)
	category           = models.ForeignKey(Category)
	victim             = models.ForeignKey(Victim)
	aggressor          = models.TextField()
	aggressor_category = models.CharField(max_length=3, choices=CATEGORY, default=COP, blank=True)
	description        = models.TextField()
	media              = models.ManyToManyField(Media, blank=True, null=True)
	features           = models.ManyToManyField(Feature)
	is_verified        = models.BooleanField()
	is_closed          = models.BooleanField()
	comments           = models.ManyToManyField(Comment, blank=True, null=True)
	created_by         = models.ForeignKey(settings.AUTH_USER_MODEL)
	created_at         = models.DateTimeField(auto_now_add=True)
	updated_at         = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		return reverse('reports:view', args=[str(self.id)])

	def __unicode__(self):
		return str(self.datetime)

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
