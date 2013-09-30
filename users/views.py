import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListHybridResponseMixin, DetailHybridResponseMixin

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
from reports.models import Victim


class UserListView(ListView):
	model = User
	template_name = "users/list.html"


class UserListHybridView(ListHybridResponseMixin, UserListView):
	pass


class UserDetailView(DetailView):
	model = User
	template_name = "users/view.html"


class UserDetailHybridView(DetailHybridResponseMixin, UserDetailView):
	pass


class UserCreateView(CreateView):
	model = User
	template_name = "users/new.html"


class UserUpdateView(UpdateView):
	model = User
	template_name = "users/edit.html"


class UserDeleteView(DeleteView):
	model = User
	template_name = "users/delete.html"
	success_url = '/users/'


def user_view(request, pk=None, username=None, extension=None):
	if pk:
		user = get_object_or_404(User, pk=pk)
	elif username:
		user = get_object_or_404(User, username=username)
	else:
		raise Http404()
	if user.pk == request.user.pk:
		return redirect('users:profile')
	if extension:
		return JSONResponse({'user': user})
	else:
		return render(request, "users/view.html", {'profile': user})


def user_profile_view(request, extension=None):
	user = request.user
	try:
		victim = Victim.objects.get(user=user)
	except Victim.DoesNotExist:
		victim = None
	if extension:
		return JSONResponse({'user': user})
	else:
		return render(request, "users/profile.html", {'profile': user, 'victim_profile': victim})


@require_POST
def user_change_password_view(request):
	logger.debug("USER PASSWORD CHANGE %s", request.POST)
	user = request.user
	user.set_password(request.POST['value'])
	user.save()
	return HttpResponse("Password changed")
	# if user.save():
	# 	return HttpResponse("Password changed")
	# else:
	# 	return HttpResponse("Unable to chage password", status=400)


@require_POST
def user_change_role_view(request):
	logger.debug("USER PASSWORD CHANGE %s", request.POST)
	user = get_object_or_404(User, pk=request.POST['pk'])
	user.role = request.POST['value']
	user.save()
	return HttpResponse("Role changed")


@require_POST
def user_deactivate_view(request, pk):
	logger.debug("USER PASSWORD DEACTIVATE %s", request.POST)
	user = get_object_or_404(User, pk=pk)
	user.is_active = False
	user.save()
	return HttpResponse("Status changed")


@require_POST
def user_activate_view(request, pk):
	logger.debug("USER PASSWORD ACTIVATE %s", request.POST)
	user = get_object_or_404(User, pk=pk)
	user.is_active = True
	user.save()
	return HttpResponse("Status changed")
