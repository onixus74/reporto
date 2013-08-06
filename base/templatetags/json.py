from django import template
from django.utils.safestring import mark_safe

from base.utils.views import dumps


register = template.Library()

@register.filter
def json(o):
    return mark_safe(dumps(o))
