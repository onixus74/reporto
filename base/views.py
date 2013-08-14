from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout

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

from django.contrib.auth.views import redirect_to_login

def home(request, *args, **kwargs):
	if request.user.is_authenticated():
		template_name = "home.html"
		context = {
			"message": "Hello!"
		}
		#context.update(csrf(request))
		#context = RequestContext(request, context)
		return render(request, template_name, context)
	else:
		#return redirect_to_login(next[, login_url, redirect_field_name])
		return redirect_to_login('home')


from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_view(request, *args, **kwargs):
	if request.user.is_authenticated():
		return redirect('home')
	form = AuthenticationForm(data = request.POST or None)
	if form.is_valid():
		user = form.get_user()
		if user.is_active:
			login(request, user)
			messages.success(request, 'Login succeeded.')
			return redirect(request.REQUEST.get('next', 'home'))
	return render(request, "login.html", {'form': form, 'next': request.REQUEST.get('next', 'home')})

	# if request.method == 'POST':
	# 	username = request.POST['username']
	# 	password = request.POST['password']
	# 	user = authenticate(username=username, password=password)
	# 	if user is not None:
	# 		if user.is_active:
	# 			login(request, user)
	# 			messages.success(request, 'Login succeeded.')
	# 			return redirect('home')
	# 		else:
	# 			return render(request, "login.html", {'form': form})
	# 	else:
	# 		#return render(request, "login-error.html")
	# 		return render(request, "login.html", {'form': form})
	# else:
	# 	return render(request, "login.html", {'form': form})


def logout_view(request, *args, **kwargs):
	logout(request)
	return redirect('home')
