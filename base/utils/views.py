from django.http import HttpResponse, Http404
from django.core import serializers
from django.views.generic.base import TemplateResponseMixin
from django.core.exceptions import ImproperlyConfigured

import json
from django.utils import simplejson

from django.views.generic import ListView, DetailView


# class JSONResponseMixin(object):
# 	def render_to_response(self, context):
# 		"Returns a JSON response containing 'context' as payload"
# 		return self.get_json_response(self.convert_context_to_json(context))

# 	def get_json_response(self, content, **httpresponse_kwargs):
# 		"Construct an `HttpResponse` object."
# 		return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

# 	def convert_context_to_json(self, context):
# 		"Convert the context dictionary into a JSON object"
# 		# Note: This is *EXTREMELY* naive; in reality, you'll need
# 		# to do much more complex handling to ensure that arbitrary
# 		# objects -- such as Django model instances or querysets
# 		# -- can be serialized as JSON.

# 		try:
# 			return serializers.serialize('json', context)
# 		except Exception, e:
# 			try:
# 				#return simplejson.dumps(context)
# 				return json.dumps(context)
# 			except Exception, e:
# 				raise e


from django.views.generic import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView
from django.views.generic.edit import BaseFormView
from django.utils import simplejson
from django.utils.encoding import force_unicode
from django.db.models.base import ModelBase
from django.db.models import ManyToManyField
from django.http import HttpResponseNotAllowed, HttpResponse
from django.core.exceptions import ImproperlyConfigured


def dumps(content, json_opts={}):
	"""
	Replaces simplejson.dumps with our own custom encoder
	"""
	json_opts['ensure_ascii'] = json_opts.get('ensure_ascii', False)
	json_opts['cls'] = json_opts.get('cls', LazyJSONEncoder)

	return simplejson.dumps(content, **json_opts)


class LazyJSONEncoder(simplejson.JSONEncoder):
	"""
	A JSONEncoder subclass that handles querysets and model objects.
	If the model object has a "serialize" method that returns a dictionary,
	then this method is used, else, it attempts to serialize fields.
	"""

	def default(self, obj):
		# This handles querysets and other iterable types
		try:
			iterable = iter(obj)
		except TypeError:
			pass
		else:
			return list(iterable)

		# This handles Models
		if isinstance(obj.__class__, ModelBase):
			if hasattr(obj, 'serialize') and callable(getattr(obj, 'serialize')):
				return obj.serialize()
			return self.serialize_model(obj)

		# Other Python Types:
		try:
			return force_unicode(obj)
		except Exception:
			pass

		# Last resort:
		return super(LazyJSONEncoder, self).default(obj)

	def serialize_model(self, obj):
		tmp = { }
		many = [f.name for f in obj._meta.many_to_many]
		for field in obj._meta.get_all_field_names( ):
			print field
			print getattr(obj, field, None)
			if len(many) > 0 and field in many:
				many.remove(field)
				tmp[field] = getattr(obj, field).all( )
			#elif :
			#	tmp[field] = getattr(obj, field, None)
			else:
				tmp[field] = getattr(obj, field, None)
		return tmp


class JSONResponse(HttpResponse):

	def __init__(self, content='', json_opts={}, mimetype="application/json", *args, **kwargs):

		if content:
			content = dumps(content, json_opts)
		else:
			content = dumps([ ], json_opts)

		super(JSONResponse, self).__init__(content,mimetype,*args,**kwargs)
		self['Cache-Control'] = 'max-age=0,no-cache,no-store'

	@property
	def json(self):
		return simplejson.loads(self.content)


class JSONResponseMixin(object):

	def render_to_response(self, context, *args, **kwargs):
		return JSONResponse(context, *args, **kwargs)

	def remove_duplicate_obj(self, context, duplicate="object", **kwargs):
		# Check if the duplicate key is in the context
		if duplicate in context:
			# Search to ensure that this key is in fact duplicated
			for key, val in context.items():
				if key == duplicate: continue           # Skip the duplicate object
				if val == context[duplicate]:
					del context[duplicate]
					break

		# Django 1.5 also adds the View...
		context.pop('view')
		return context


class JSONDataView(JSONResponseMixin, View):

	def get_context_data(self, **kwargs):
		return kwargs

	def get(self, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)


class JSONDetailView(JSONResponseMixin, BaseDetailView):
	"""
	Override get method to allow access from querystrings for AJAX calls.
	"""

	def get(self, request, **kwargs):
		"""
		This method does not allow multiple parameters in the query string,
		so a normal dictionary rather than a QueryDict is necessary.

		The development version has a QuerySet.dict method-- but not 1.3, so
		we have to do this manually until the new version comes out.
		"""
		querydict = dict([(k,v) for k,v in request.GET.iteritems()])
		self.kwargs.update(querydict)
		kwargs.update(querydict)
		return super(JSONDetailView, self).get(request, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(JSONDetailView, self).get_context_data(**kwargs)
		return self.remove_duplicate_obj(context)


class JSONListView(JSONResponseMixin, BaseListView):

	def get_context_data(self, **kwargs):
		context = super(JSONListView, self).get_context_data(**kwargs)
		return self.remove_duplicate_obj(context, duplicate="object_list")


class PaginatedJSONListView(JSONListView):
	"""
	Provides some helper view methods and a default pagination for the
	ListView -- including removal of pagination data from the json and a
	json return of the total number of results and pages that will be
	returned on the submission of a get request.
	"""

	paginate_by = 10
	count_query = 'count'
	count_only  = False

	def get_count_query(self):
		return self.count_query

	def get_count_only(self):
		return self.count_only

	def get(self, request, *args, **kwargs):
		"""
		On GET if the parameter defined by ``count_query`` is in the
		request, then set the count only parameter to True. Note that the
		method ``get_count_only`` can override or use this value as
		required -- but the interface is to set the value on the instance.
		"""
		if self.get_count_query() in self.request.GET:
			self.count_only = True
		return super(PaginatedJSONListView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		"""
		Removes paginator objects and instead supplies the pages and the
		count data as part of the paginated framework. Leaves in the
		``is_paginated`` boolean value.

		Also tests to see if get_count_only is True -- if so, it returns
		only the pages and the count rather than the entire context.
		"""
		context = super(PaginatedJSONListView, self).get_context_data(**kwargs)

		# Replace paginatior data with JSON friendly data
		page       = context.pop('page_obj')
		paginator  = context.pop('paginator')
		count_only = self.get_count_only()

		if paginator:
			pages = paginator.num_pages
			count = paginator.count
			ispag = page.has_other_pages()
			ppage = paginator.per_page
			cpage = page.number
		else:
			# Honestly, this should never happen.
			page  = 1
			pages = 1
			count = self.get_queryset().count()  # This should be the object_list that comes through...
			ispag = False
			ppage = count
			cpage = 1

		if count_only:
			return { 'pages':pages,
					 'count':count,
					 'per_page': ppage,
					 'is_paginated': ispag,
					 'current': cpage, }
		else:
			context['pages'] = pages
			context['count'] = count
			context['current'] = cpage

		return context


class JSONFormView(JSONResponseMixin, BaseFormView):
	"""
	An attempt to integrate a JSONView with a FormView.

	Basically, the idea is this- JSON views will not require a GET method.
	Since POST is the only concern, we need to pass the post data into
	the form, then respond with JSON data instead of Form data.

	Several Overrides are the attempt to manipulate the BaseFormView to
	respond with JSON data, rather than starting from scratch.
	"""

	def get_form_class(self):
		"""
		There will be issues if form_class is None, so override this
		method to check and see if we have one or not.
		"""
		form_class = super(JSONFormView, self).get_form_class()
		if form_class is None:
			raise ImproperlyConfigured(
				"No form class to validate. Please set form_class on"
				" the view or override 'get_form_class()'.")
		return form_class

	def get_success_url(self):
		"""
		Overridden to ensure that JSON data gets returned, rather
		than HttpResponseRedirect, which is bad.
		"""
		return None

	def form_valid(self, form):
		"""
		Overridden to ensure that an HttpResponseRedirect does not get
		called with a success_url -- instead render_to_response some
		JSON data. DO NOT CALL SUPER!

		@note: We return a JSON flag - { success: true }. Because this
		is a common paradigm in Ben programming. However, it seems that
		the flag should be { valid: true }. Discuss amongst yourselves.
		"""
		return self.render_to_response(self.get_context_data(success=True))

	def form_invalid(self, form):
		"""
		Overridden to ensure that a form object isn't returned, since
		that has some weird serialization issues. Instead pass back
		the errors from the form, and a JSON flag - { success: false }.

		@note: See form_valid for more discussion on the JSON flag.
		"""
		context = self.get_context_data(success=False)
		context['errors'] = form.errors
		return self.render_to_response(context)

	def get(self, request, *args, **kwargs):
		"""
		Overridden so that on a GET request the response isn't allowed.

		JSON Forms are intrinsinctly POST driven things, a GET makes
		no sense in the context of a form. (What would you get?). For
		Normal HTTP, you would pass back an empty form, but that's
		pretty usesless for JSON. So we pwn this entire method right
		off the bat to ensure no screwiness or excessive net traffic.
		"""
		return HttpResponseNotAllowed(['GET',])





class HybridResponseMixin(JSONResponseMixin):
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


class ListHybridResponseMixin(HybridResponseMixin, JSONListView):
	default_view = ListView

class PaginatedListHybridResponseMixin(HybridResponseMixin, PaginatedJSONListView):
	default_view = ListView

class DetailHybridResponseMixin(HybridResponseMixin, JSONDetailView):
	default_view = DetailView





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








class HybridFormatResponseMixin(TemplateResponseMixin):
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
		class AdCategoryListView(HybridFormatResponseMixin, ListView):

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
						return super(HybridFormatResponseMixin, self).render_to_response(context) # call original ListView.render_to_response()
				elif self.request.GET.get('output','') == 'inc.html':
						opts = self.get_queryset().model._meta
						self.template_name = "%s/%s%s.inc.html" % (opts.app_label, opts.object_name.lower(), self.template_name_suffix)
						return super(HybridFormatResponseMixin, self).render_to_response(context) # call original ListView.render_to_response()

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











import json

from django.http import HttpResponse
from django.views.generic.edit import CreateView

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return self.render_to_json_response(data)
        else:
            return response

# class AuthorCreate(AjaxableResponseMixin, CreateView):
#     model = Author
