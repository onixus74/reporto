# from django.core.serializers import serialize
# from django.db.models.query import QuerySet
# from django.utils import simplejson
# from django.template import Library

# register = Library()

# def json(object):
#     if isinstance(object, QuerySet):
#         return serialize('json', object)
#     return simplejson.dumps(object)

# register.filter('jsonify', jsonify)


from django import template
from django.utils.safestring import mark_safe
from django.utils import simplejson

register = template.Library()

@register.filter
def jsonn(o):
    return mark_safe(simplejson.dumps(o))
