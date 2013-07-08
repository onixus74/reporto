from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request, *args, **kwargs):
	template_name = "report_submission/index.html"
	context = {
		"message": "Hello!"
	}
	return render_to_response(template_name, context)

