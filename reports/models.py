from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, Permission

class Category(models.Model):
	slug       = models.SlugField(max_length=100)
	definition = models.CharField(max_length=300)

	def get_absolute_url(self):
		return reverse('categories:view', args=[str(self.id)])

	def __unicode__(self):
		return self.definition


class Feature(models.Model):
	slug       = models.SlugField(max_length=200)
	definition = models.CharField(max_length=300)

	def get_absolute_url(self):
		return reverse('features:view', args=[str(self.id)])

	def __unicode__(self):
		return self.definition


class Media(models.Model):
	title        = models.CharField(max_length=200)
	description  = models.TextField()
	url          = models.CharField(max_length=300)
	external_url = models.CharField(max_length=300)
	folder       = models.CharField(max_length=300)


	#COMMENT = 'C'
	#CATEGORY = (
	#	(COMMENT, "Comment"),
	#)
	#category = models.CharField(max_length=1, choices=CATEGORY, default=COMMENT, blank=True)

	def __unicode__(self):
		return self.definition


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


	def get_absolute_url(self):
		return reverse('victims:view', args=[str(self.id)])

	def __unicode__(self):
		return self.firstname + " " + self.lastname


class Report(models.Model):

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
	media_folder       = models.CharField(max_length=300, blank=True, null=True)
	media_urls         = models.TextField(blank=True, null=True)
	#media              = models.ManyToManyField(Media)
	features           = models.ManyToManyField(Feature)
	#comments           = models.ManyToManyField(Comment)
	is_verified        = models.BooleanField()
	is_closed          = models.BooleanField()
	#Ministry Response?
	created_by         = models.ForeignKey(User)
	created_at         = models.DateTimeField(auto_now_add=True)
	updated_at         = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		return reverse('reports:view', args=[str(self.id)])

	def __unicode__(self):
		return str(self.datetime)

	class Meta:
		ordering = ["datetime"]


class Comment(models.Model):
	content    = models.TextField()
	report     = models.ForeignKey(Report)
	created_by = models.ForeignKey(User)
	created_at = models.DateTimeField(auto_now_add=True)
	#updated_at = models.DateTimeField(auto_now=True)
