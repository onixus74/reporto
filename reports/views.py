from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def index(request, *args, **kwargs):
	template_name = "reports/index.html"
	context = {
		"message": "Hello!"
	}
	return render_to_response(template_name, context)

def dashboard(request, *args, **kwargs):
	template_name = "reports/dashboard.html"
	context = {
		"message": "Hello!"
	}
	return render_to_response(template_name, context)

def submission(request, *args, **kwargs):
	template_name = "reports/submission.html"
	context = {
		"message": "Hello!"
	}
	return render_to_response(template_name, context)

