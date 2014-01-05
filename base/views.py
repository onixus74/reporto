import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext as _

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
#from django.contrib.auth.views import redirect_to_login
#from django.core.context_processors import csrf
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
#from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _

from base.utils.views import JSONResponse
from appreciations.models import Report as AppreciationReport
from users.forms import UserCreationForm
from users.models import User
from django.contrib.auth.models import Group
from violations.models import Report as ViolationReport
from violations.views import append_violations_statistics, append_appreciations_statistics


@csrf_exempt
def test_view(request, *args, **kwargs):
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


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')


#from crispy_forms.helper import FormHelper


class UserCreationForm(UserCreationForm):
    #email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


def signup_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('home')
    form = UserCreationForm(request.POST or None)

    # form.helper = FormHelper(form)
    # form.helper.form_class = "form-horizontal"
    # form.helper.label_class = "col-lg-4"
    # form.helper.field_class = "col-lg-8"

    if form.is_valid():
        user = form.save()

        if user.is_active:
            #logger.debug('SIGNUP %s', [user, user.username, user.password, request.POST["password"], form.cleaned_data["password"]])
            user = authenticate(username=user.username, password=form.cleaned_data["password"])
            #logger.debug('SIGNUP %s', [user])
            login(request, user)
            #messages.success(request, 'Sign in succeeded.')
            # return redirect(request.REQUEST.get('next', 'users:profile'))
            return redirect('users:profile')
        else:
            messages.warning(request, 'Sorry, your user account is inactive.')
    return render(request, "signup.html", {'form': form, 'next': request.REQUEST.get('next', '/')})


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('home')
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        if user.is_active:
            login(request, user)
            #messages.success(request, 'Sign in succeeded.')
            return redirect(request.REQUEST.get('next', '/'))
        else:
            messages.warning(request, 'Sorry, your user account is inactive.')

    return render(request, "login.html", {
        'form': form,
        'next': request.REQUEST.get('next', '/'),
        'violations_count': ViolationReport.objects.count(),
        'violations_latest': ViolationReport.objects.all()[:3],
        'violations_top_reporters': [{'get_full_name': item['created_by__first_name'] + ' ' + item['created_by__last_name'], 'count': item['count']} for item in ViolationReport.objects.values('created_by__first_name', 'created_by__last_name').annotate(count=Count('id')).order_by('-count')[:3]],
        'violations_top_reporting_circles': [{'name': item['created_by__groups__name'], 'count': item['count']} for item in ViolationReport.objects.values('created_by__groups__name',).annotate(count=Count('id')).order_by('-count')[:3]],
        'appreciations_count': AppreciationReport.objects.count(),
        'appreciations_latest': AppreciationReport.objects.all()[:3],
        'appreciations_top_reporters': [{'get_full_name': item['created_by__first_name'] + ' ' + item['created_by__last_name'], 'count': item['count']} for item in AppreciationReport.objects.values('created_by__first_name', 'created_by__last_name').annotate(count=Count('id')).order_by('-count')[:3]],
        'appreciations_top_reporting_circles': [{'name': item['created_by__groups__name'], 'count': item['count']} for item in AppreciationReport.objects.values('created_by__groups__name',).annotate(count=Count('id')).order_by('-count')[:3]],
    })


    # if request.method == 'POST':
    # 	username = request.POST['username']
    # 	password = request.POST['password']
    # 	user = authenticate(username=username, password=password)
    # 	if user is not None:
    # 		if user.is_active:
    # 			login(request, user)
    # 			messages.success(request, 'Sign in succeeded.')
    # 			return redirect('home')
    # 		else:
    # 			return render(request, "login.html", {'form': form})
    # 	else:
    # return render(request, "login-error.html")
    # 		return render(request, "login.html", {'form': form})
    # else:
    # 	return render(request, "login.html", {'form': form})

def login_minimal_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('home')
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        if user.is_active:
            login(request, user)
            #messages.success(request, 'Sign in succeeded.')
            return redirect(request.REQUEST.get('next', '/'))
        else:
            messages.warning(request, 'Sorry, your user account is inactive.')

    return render(request, "login-minimal.html", {
        'form': form,
        'next': request.REQUEST.get('next', '/')
    })


def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('home')

paginate_by = 5


def home_view(request, *args, **kwargs):
    if not request.user.is_authenticated():
        return login_view(request, *args, **kwargs)
    # if request.user.is_authenticated():
    template_name = "home.html"
    context = {}

    violations = ViolationReport.objects.all()
    violations_paginator = Paginator(violations, paginate_by)

    violations_page = request.GET.get('violations-page')
    try:
        violations = violations_paginator.page(violations_page)
    except PageNotAnInteger:
        violations_page = 1
        violations = violations_paginator.page(violations_page)
    except EmptyPage:
        violations_page = violations_paginator.num_pages
        violations = violations_paginator.page(violations_page)

    context['violations_list'] = violations
    context['violations_pagination'] = {
        'count': violations_paginator.count,
        'pages': violations_paginator.num_pages,
        'current': violations.number,
        'is_paginated': violations_paginator.num_pages > 1
    }

    appreciations = AppreciationReport.objects.all()
    appreciations_paginator = Paginator(appreciations, paginate_by)

    appreciations_page = request.GET.get('appreciations-page')
    try:
        appreciations = appreciations_paginator.page(appreciations_page)
    except PageNotAnInteger:
        appreciations_page = 1
        appreciations = appreciations_paginator.page(appreciations_page)
    except EmptyPage:
        appreciations_page = appreciations_paginator.num_pages
        appreciations = appreciations_paginator.page(appreciations_page)

    context['appreciations_list'] = appreciations
    context['appreciations_pagination'] = {
        'count': appreciations_paginator.count,
        'pages': appreciations_paginator.num_pages,
        'current': appreciations.number,
        'is_paginated': appreciations_paginator.num_pages > 1
    }

    append_violations_statistics(context)
    append_appreciations_statistics(context)

    context['violations_locations'] = ViolationReport.objects.values('latitude', 'longitude', 'category__definition', 'pk')
    context['appreciations_locations'] = AppreciationReport.objects.values('latitude', 'longitude', 'category__definition', 'pk')

    #context = RequestContext(request, context)
    # context.update(csrf(request))
    return render(request, template_name, context)
    # else:
    # return redirect_to_login(next[, login_url, redirect_field_name])
    # return redirect_to_login('/')


@require_http_methods(['OPTIONS', 'GET'])
def statistics_view(request, *args, **kwargs):
    if request.method == 'OPTIONS':
        response = HttpResponse()
    else:
        response = {}

        append_violations_statistics(response)
        append_appreciations_statistics(response)

        response = JSONResponse(response)

    response['Access-Control-Allow-Origin'] = '*'
    return response
