
import logging

from crispy_forms.helper import FormHelper
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_form
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from base.utils.views import dumps
import markdown as markdown_lib


logger = logging.getLogger(__name__)


register = template.Library()


@register.filter
def json(obj):
    return mark_safe(dumps(obj))


@register.filter
def times(number):
    return range(number)


@register.filter
def keys(object):
    return [key for key in dict(object)]


@register.filter
def values(dict):
    return [object[key] for key in dict(object)]


@register.filter
def pluck(list, key):
    return [i.get(key, None) for i in list]


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


@register.filter
def crispy_form_horizontal(form, config='col-md-4,col-md-8'):
    label_class, field_class = config.split(',')
    form = as_crispy_form(form, label_class=label_class, field_class=field_class)
    return form


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    extensions = ["nl2br", ]
    return mark_safe(markdown_lib.markdown(force_unicode(value),
                                           extensions,
                                           safe_mode=True,
                                           enable_attributes=False))


class SetVarNode(template.Node):
    def __init__(self, new_val, var_name):
        self.new_val = new_val
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = self.new_val
        return ''

import re

@register.tag
def setvar(parser,token): # {% setvar "a string" as new_template_var %}
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    new_val, var_name = m.groups()
    if not (new_val[0] == new_val[-1] and new_val[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return SetVarNode(new_val[1:-1], var_name)

