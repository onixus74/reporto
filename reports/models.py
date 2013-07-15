from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
	slug = models.SlugField(max_length=100)
	definition = models.CharField(max_length=300)

	def get_absolute_url(self):
		return reverse('categories:view', args=[str(self.id)])

	def __unicode__(self):
		return self.definition


class Feature(models.Model):
	slug = models.SlugField(max_length=200)
	definition = models.CharField(max_length=300)

	def get_absolute_url(self):
		return reverse('features:view', args=[str(self.id)])

	def __unicode__(self):
		return self.definition

class Media(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	url = models.CharField(max_length=300)
	external_url = models.CharField(max_length=300)


class Victim(models.Model):

	MALE = 'M'
	FEMALE = 'F'
	GENDER = (
		(MALE, 'Male'),
		(FEMALE, 'Female')
	)

	fullname    = models.CharField(max_length=200)
	gender      = models.CharField(max_length=1, choices=GENDER, default=MALE)
	age         = models.PositiveIntegerField()
	education   = models.CharField(max_length=200)
	profession  = models.CharField(max_length=200)
	phone       = models.CharField(max_length=20)
	email       = models.EmailField()
	description = models.TextField()

	def get_absolute_url(self):
		return reverse('victims:view', args=[str(self.id)])

	def __unicode__(self):
		return self.fullname

class Report(models.Model):

	datetime = models.DateTimeField('date and time')
	location = models.CharField(max_length=100)
	location_text = models.CharField(max_length=300)
	category = models.ForeignKey(Category)
	victim = models.ForeignKey(Victim)
	aggressor = models.TextField()
	description = models.TextField()
	#media = models.ForeignKey(Media)
	features = models.ManyToManyField(Feature)
	is_verified = models.BooleanField()
	is_closed = models.BooleanField()
	#Ministry Response:

	def get_absolute_url(self):
		return reverse('reports:view', args=[str(self.id)])

	def __unicode__(self):
		return str(self.datetime)
