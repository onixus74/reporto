from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import model_to_dict


class User(AbstractUser):

    # class Meta:
    #	unique_together = ('email', )

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    #REQUIRED_FIELDS = ['first_name', 'last_name']
    #USERNAME_FIELD = 'email'

    report_builder_exclude_fields = ('email', 'password')

    REPORTER = "R"
    MODERATOR = "M"
    ADMIN = "A"
    ROLE = (
        (REPORTER,  "Reporter"),
        (MODERATOR, "Moderator"),
        (ADMIN,     "Administrator"),
    )

    role = models.CharField(max_length=1, choices=ROLE, default=REPORTER)

    def get_absolute_url(self):
        return reverse('users:view', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        self.username = self.email
        # self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    def serialize(self):
        data = model_to_dict(self, fields=['id', 'first_name', 'last_name', 'role'])
        data['short_name'] = self.get_short_name()
        data['full_name'] = self.get_full_name()
        data['role_display'] = self.get_role_display()
        # data.pop('email')
        # data.pop('username')
        return data

    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    def is_moderator(self):
        return self.role == self.MODERATOR

    def is_reporter(self):
        return self.role == self.REPORTER


email = User._meta.get_field_by_name('email')[0]
email.null = False
email.blank = False
email._unique = True

username = User._meta.get_field_by_name('username')[0]
username.null = True
username.blank = True
#username._unique = False

first_name = User._meta.get_field_by_name('first_name')[0]
first_name.null = False
first_name.blank = False

last_name = User._meta.get_field_by_name('last_name')[0]
last_name.null = False
last_name.blank = False
