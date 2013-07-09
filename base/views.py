from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request, *args, **kwargs):
	template_name = "home.html"
	context = {
		"message": "Hello!"
	}
	return render_to_response(template_name, context)


