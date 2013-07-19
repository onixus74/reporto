from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request, *args, **kwargs):
	template_name = "home.html"
	context = {
		"message": "Hello!"
	}
	return render_to_response(template_name, context)


@csrf_exempt
def test(request, *args, **kwargs):
	print "session:", request.session.items()
	print "method:", request.method
	#print "body:", request.body
	print "content-type:", request.META['CONTENT_TYPE']
	print "cookies:", request.COOKIES
	print "request:", request.REQUEST
	print "get:", request.GET
	print "post:", request.POST
	print "files:", request.FILES
	#return HttpResponse({'done': True})
	return render_to_response('test.html', {'done': True})
