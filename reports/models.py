from django.db import models
from django.core.urlresolvers import reverse


class Category(models.Model):
	slug = models.SlugField(max_length=100)
	definition = models.CharField(max_length=300)

	def get_absolute_url(self):
		return reverse('categories:view', args=[str(self.id)])

	def __unicode__(self):
		return u"Slug:%s; Definition: %s" % (self.slug, self.definition)


class Feature(models.Model):
	slug = models.SlugField(max_length=200)
	definition = models.CharField(max_length=300)


class Media(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=300)
	url = models.CharField(max_length=300)
	external_url = models.CharField(max_length=300)


class Victim(models.Model):
	fullname = models.CharField(max_length=200)


class Report(models.Model):
	# ...
	pub_date = models.DateTimeField('date published')
	category = models.ForeignKey(Category)
	feature = models.ForeignKey(Feature)
	media = models.ForeignKey(Media)

