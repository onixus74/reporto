from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

#class User(AbstractBaseUser):
#	username = models.CharField(max_length=40, unique=True, db_index=True)
#	USERNAME_FIELD = 'username'

class User(AbstractUser):

	def get_absolute_url(self):
		return reverse('users:view', args=[str(self.id)])

	def fullname(self):
		return self.first_name + ' ' + self.last_name

	def __unicode__(self):
		return self.fullname() + ' (' + self.username + ')'
