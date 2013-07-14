from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.generic.base import TemplateResponseMixin
from django.core.exceptions import ImproperlyConfigured

import json
from django.utils import simplejson

from django.views.generic import ListView, DetailView


class JSONResponseMixin(object):
	def render_to_response(self, context):
		"Returns a JSON response containing 'context' as payload"
		return self.get_json_response(self.convert_context_to_json(context))

	def get_json_response(self, content, **httpresponse_kwargs):
		"Construct an `HttpResponse` object."
		return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

	def convert_context_to_json(self, context):
		"Convert the context dictionary into a JSON object"
		# Note: This is *EXTREMELY* naive; in reality, you'll need
		# to do much more complex handling to ensure that arbitrary
		# objects -- such as Django model instances or querysets
		# -- can be serialized as JSON.

		try:
			return serializers.serialize('json', context)
		except Exception, e:
			try:
				#return simplejson.dumps(context)
				return json.dumps(context)
			except Exception, e:
				raise e


class MultiResponseMixin(JSONResponseMixin):
	default_view = None
	def render_to_response(self, context):
		print self.request.META['CONTENT_TYPE']
		print context
		# Look for '.json' URL extension, 'format=json' GET argument or 'application/json' accept header in request
		is_json = self.kwargs.get('extension', None) == "json" or self.request.GET.get('format', None) == "json"
		#print format
		if is_json:
			return JSONResponseMixin.render_to_response(self, context)
		else:
			return self.default_view.render_to_response(self, context)


class ListMultiResponseMixin(MultiResponseMixin):
	default_view = ListView

	def convert_context_to_json(self, context):
		return serializers.serialize('json', context['object_list'])


class DetailMultiResponseMixin(MultiResponseMixin):
	default_view = DetailView

	def convert_context_to_json(self, context):
		return serializers.serialize('json', [context['object']])
		#return json.dumps(context['object'])


from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
from django.template import Library

register = Library()

def jsonify(object):
	if isinstance(object, QuerySet):
		return serialize('json', object)
	return simplejson.dumps(object)

register.filter('jsonify', jsonify)
# class SFH_Get_Region_View(JSONResponseMixin, BaseDetailView):
#     def get(self, request, *args, **kwargs):
#         #do some queries here to collect your data for the response
#         json_response = "This ain't no country for old men"

#         context = {'success':json_response}
#         return self.render_to_response(context)








class MultiFormatResponseMixin(TemplateResponseMixin):
    """
    Render http response in in either in HTML (default), HTML snippet or any serializer that is supported format.
    The rendering output is determined by ``output`` request GET variable  as follows:

    ``?output=serialzier_<serializer_name> OR <html> OR <inc.html>`` - OPTIONAL: defaults to html

    <serializer_name> part of the GET variable is passed to the Django serialzier frame with additional ``serializer_options``
    defined on your custom class views. Hence if one has added additional serialziers they are fully supported.

    If <serializer_name> dosen't exist or output serializer format is not supported or serializer_options are missing
     a 404 response is generated.

    To use simple define your class based view as follows and based on ?output=<value> different format is returned:

    ```
    class AdCategoryListView(MultiFormatResponseMixin, ListView):

    context_object_name="adcategories_list"
    serializer_options = {
                    'json': {
                            'fields': ['locations'],
                            'extras': ['get_firstmedia_url']
                            },
                    'geojson': {
                            'fields': ['locations'],
                            }
                    }

    def get_queryset(self):
        return AdCategory.objects.filter(parent_category__isnull = True)

    ...
    ...

    ```

    Template naming convention for different outputs:

    ```?output=serialzier_json``` = NO TEMPLATE - response is output of calling json serialzier on the query
    ```?output=serialzier_foobar``` = NO TEMPLATE - response is output of calling foobar serialzier on the query


    ```?output=html``` = <templates>/<app_label>/<model name><template_name_suffix>.html
    ```?output=inc.html``` = <templates>/<app_label>/<model name><template_name_suffix>.inc.html

    Suggested aditional serialziers:
        GEOJSON - http://djangosnippets.org/snippets/2434/)
        DjangoFullSerializers http://code.google.com/p/wadofstuff/wiki/DjangoFullSerializers

    """
    def render_to_response(self, context):
        # Look for a 'format=<foo>' GET argument if dosen't exist then do normal html Template Response mixin response
        if self.request.GET.get('output','html') == 'html':
            return super(MultiFormatResponseMixin, self).render_to_response(context) # call original ListView.render_to_response()
        elif self.request.GET.get('output','') == 'inc.html':
            opts = self.get_queryset().model._meta
            self.template_name = "%s/%s%s.inc.html" % (opts.app_label, opts.object_name.lower(), self.template_name_suffix)
            return super(MultiFormatResponseMixin, self).render_to_response(context) # call original ListView.render_to_response()

        output = self.request.GET.get('output')
        if not 'serializer_' in output:
            raise Http404

        """
        Check we are configured properly first - we do the check here so that adding this mixin
        dosen't prevent original view logic from executing
        """
        if not hasattr(self, 'serializer_options'):
            raise ImproperlyConfigured(u"'%s' must define 'serializer_options'" % self.__class__.__name__)

        serializer = output.split('_')[1] # grap serialzier name

        """ if serialzier is not supported or it's options not specified in view's serializer_options raise 404"""
        if not serializer in serializers.get_serializer_formats() or serializer not in self.serializer_options:
            raise Http404

        output = self.request.GET.get('output','')
        query = self.get_queryset()
        if hasattr(self, 'get_object'): # if get_object attribute exists than we should filter to that object only
            query = query.filter(pk=self.get_object().pk)

        content = serializers.serialize(serializer, query, **self.serializer_options[serializer])
        #return HttpResponse(content, content_type='application/%s' % serializer)
        return HttpResponse(content)


