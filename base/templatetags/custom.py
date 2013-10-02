from django import template
from django.utils.safestring import mark_safe

from base.utils.views import dumps


register = template.Library()

@register.filter
def json(obj):
	return mark_safe(dumps(obj))

@register.filter
def times(number):
	return range(number)
