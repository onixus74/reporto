from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

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
	return render(request, 'test.html', {'done': True})


from django.core.context_processors import csrf


def home(request, *args, **kwargs):
	if request.user.is_authenticated():
		template_name = "home.html"
		context = {
			"message": "Hello!"
		}
	else:
		template_name = "nologin.html"
		context = {}
	#context.update(csrf(request))
	#context = RequestContext(request, context)
	return render(request, template_name, context)


from django.contrib.auth import authenticate, login, logout


def login_view(request, *args, **kwargs):
	if request.method == 'POST':
		username = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('home')
			else:
				return redirect('home')
		else:
			#return render(request, "login-error.html")
			return render(request, "login.html")
	else:
		return render(request, "login.html")


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('home')
