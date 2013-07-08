from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from reports.models import Category

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
		"items": Category.objects.all()
	}
	return render_to_response(template_name, context)

