import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib import messages
from base.utils.views import JSONResponse

from users.models import User


@csrf_exempt
def test(request, *args, **kwargs):
	logger.debug("session: %s", request.session.items())
	logger.debug("method: %s", request.method)
	#logger.debug("body: %s", request.body)
	logger.debug("content-type: %s", request.META['CONTENT_TYPE'])
	logger.debug("cookies: %s", request.COOKIES)
	logger.debug("request: %s", request.REQUEST)
	logger.debug("get: %s", request.GET)
	logger.debug("post: %s", request.POST)
	logger.debug("files: %s", request.FILES)
	#return HttpResponse({'done': True})
	return render(request, 'test.html', {'done': True})


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
		return redirect_to_login('/')


def login_view(request, *args, **kwargs):
	if request.user.is_authenticated():
		return redirect('home')
	form = AuthenticationForm(data = request.POST or None)
	if form.is_valid():
		user = form.get_user()
		if user.is_active:
			login(request, user)
			messages.success(request, 'Login succeeded.')
			return redirect(request.REQUEST.get('next', '/'))
		else:
			messages.warning(request, 'Sorry, your user account is inactive.')
	return render(request, "login.html", {'form': form, 'next': request.REQUEST.get('next', '/')})

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

