
import logging
logger = logging.getLogger(__name__)


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


from crispy_forms.helper import FormHelper


@register.filter
def crispy_form_horizontal_(form):
    logger.debug('FORM %s', form)
    form.helper = FormHelper(form)
    logger.debug('HELPER %s', form.helper)
    logger.debug('FORM %s', form)
    form.helper.form_class = "form-horizontal"
    form.helper.label_class = "col-lg-4"
    form.helper.field_class = "col-lg-8"
    return form

from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form


@register.filter
def crispy_form_horizontal(form, config='col-md-4,col-md-8'):
    label_class, field_class = config.split(',')
    form = as_crispy_form(form, label_class=label_class, field_class=field_class)
    return form

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
