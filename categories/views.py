from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# list()
# list() for for XHR
# view(id)
# edit(id)
# update(id) for XHR
# delete(id)
# delete(id) for XHR

def list(request, *args, **kwargs):
	template_name = "categories/list.html"
	context = {
		"items": [
			{'id': 1, 'slug': "cat-1", 'definition': "Category 1"},
			{'id': 2, 'slug': "cat-2", 'definition': "Category 2"},
			{'id': 3, 'slug': "cat-3", 'definition': "Category 3"},
		]
	}
	return render_to_response(template_name, context)

