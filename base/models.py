from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

from django.forms.models import model_to_dict


class User(AbstractUser):

	REPORTER  = "R"
	MODERATOR = "M"
	ADMIN     = "A"
	ROLE = (
		(REPORTER,  "Reporter"),
		(MODERATOR, "Moderator"),
		(ADMIN,     "Administrator"),
	)

	role = models.CharField(max_length=1, choices=ROLE, default=REPORTER)

	def get_absolute_url(self):
		return reverse('users:view', args=[str(self.id)])

	def __unicode__(self):
		return self.get_full_name() + ' (@' + self.username + ')'

	def serialize(self):
		data = model_to_dict(self, fields=['id', 'username', 'first_name', 'last_name', 'role'])
		data['short_name'] = self.get_short_name()
		data['full_name'] = self.get_full_name()
		data['role_display'] = self.get_role_display()
		return data
