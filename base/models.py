from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

#class User(AbstractBaseUser):
#	username = models.CharField(max_length=40, unique=True, db_index=True)
#	USERNAME_FIELD = 'username'

class User(AbstractUser):

	REPORTER  = "R"
	MODERATOR = "M"
	ADMIN     = "A"
	ROLE = (
		(REPORTER, "Reporter"),
		(MODERATOR, "Moderator"),
		(ADMIN, "Administrator"),
	)

	role = models.CharField(max_length=1, choices=ROLE, default=REPORTER, blank=True)

	def get_absolute_url(self):
		return reverse('users:view', args=[str(self.id)])

	def fullname(self):
		return self.first_name + ' ' + self.last_name

	def __unicode__(self):
		return self.fullname() + ' (@' + self.username + ')'

	def serialize(self):
		return {
			'id': self.id,
			'username': self.username,
			'firstname': self.first_name,
			'lastname': self.last_name,
			'fullname': self.fullname(),
		}
