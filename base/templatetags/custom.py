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


import markdown as markdown_lib

from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    extensions = ["nl2br", ]
    return mark_safe(markdown_lib.markdown(force_unicode(value),
                                           extensions,
                                           safe_mode=True,
                                           enable_attributes=False))
