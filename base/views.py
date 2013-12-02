import logging
logger = logging.getLogger(__name__)

from django import forms
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
from users.forms import UserCreationForm

from reports.models import Report, ThankReport
from reports.views import append_statistics


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
    # return HttpResponse({'done': True})
    return render(request, 'test.html', {'done': True})


def home(request, *args, **kwargs):
    if request.user.is_authenticated():
        template_name = "home.html"
        context = {
            "message": "Hello!"
        }
        # context.update(csrf(request))
        #context = RequestContext(request, context)
        return render(request, template_name, context)
    else:
        # return redirect_to_login(next[, login_url, redirect_field_name])
        return redirect_to_login('/')


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')


def register_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('home')
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()

        if user.is_active:
            #logger.debug('REGISTRATION %s', [user, user.username, user.password, request.POST["password"], form.cleaned_data["password"]])
            user = authenticate(username=user.username, password=form.cleaned_data["password"])
            #logger.debug('REGISTRATION %s', [user])
            login(request, user)
            messages.success(request, 'Login succeeded.')
            #return redirect(request.REQUEST.get('next', 'users:profile'))
            return redirect('users:profile')
        else:
            messages.warning(request, 'Sorry, your user account is inactive.')
    return render(request, "register.html", {'form': form, 'next': request.REQUEST.get('next', '/')})


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('home')
    form = AuthenticationForm(data=request.POST or None)
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
    # return render(request, "login-error.html")
    # 		return render(request, "login.html", {'form': form})
    # else:
    # 	return render(request, "login.html", {'form': form})


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('home')


def home_dashboard(request, *args, **kwargs):
    #if request.user.is_authenticated():
    template_name = "home_dashboard.html"
    context = {}

    context['report_list'] = Report.objects.all();
    context['thankreport_list'] = ThankReport.objects.all();

    append_statistics(context)

    context['incidents_locations'] = Report.objects.values('latitude', 'longitude', 'category__definition', 'pk')
    context['thanks_locations'] = ThankReport.objects.values('latitude', 'longitude', 'category__definition', 'pk')

    #context = RequestContext(request, context)
    # context.update(csrf(request))
    return render(request, template_name, context)
    #else:
    # return redirect_to_login(next[, login_url, redirect_field_name])
    # return redirect_to_login('/')
