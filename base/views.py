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

from incidents.models import Report, ThankReport
from incidents.views import append_incidents_statistics, append_thanks_statistics


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


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')


from crispy_forms.helper import FormHelper


def register_view(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('home')
    form = UserCreationForm(request.POST or None)
    form.helper = FormHelper(form)
    form.helper.form_class = "form-horizontal"
    form.helper.label_class = "col-lg-4"
    form.helper.field_class = "col-lg-8"
    if form.is_valid():
        user = form.save()

        if user.is_active:
            #logger.debug('REGISTRATION %s', [user, user.username, user.password, request.POST["password"], form.cleaned_data["password"]])
            user = authenticate(username=user.username, password=form.cleaned_data["password"])
            #logger.debug('REGISTRATION %s', [user])
            login(request, user)
            messages.success(request, 'Login succeeded.')
            # return redirect(request.REQUEST.get('next', 'users:profile'))
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

paginate_by = 5

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request, *args, **kwargs):
    # if request.user.is_authenticated():
    template_name = "home.html"
    context = {}

    incidents = Report.objects.all()
    incidents_paginator = Paginator(incidents, paginate_by)

    incidents_page = request.GET.get('incidents-page')
    try:
        incidents = incidents_paginator.page(incidents_page)
    except PageNotAnInteger:
        incidents_page = 1
        incidents = incidents_paginator.page(incidents_page)
    except EmptyPage:
        incidents_page = incidents_paginator.num_pages
        incidents = incidents_paginator.page(incidents_page)

    context['report_list'] = incidents
    context['report_pagination'] = {
        'count': incidents_paginator.count,
        'pages': incidents_paginator.num_pages,
        'current': incidents.number,
        'is_paginated': incidents_paginator.num_pages > 1
    }

    thanks = ThankReport.objects.all()
    thanks_paginator = Paginator(thanks, paginate_by)

    thanks_page = request.GET.get('thanks-page')
    try:
        thanks = thanks_paginator.page(thanks_page)
    except PageNotAnInteger:
        thanks_page = 1
        thanks = thanks_paginator.page(thanks_page)
    except EmptyPage:
        thanks_page = thanks_paginator.num_pages
        thanks = thanks_paginator.page(thanks_page)

    context['thankreport_list'] = thanks
    context['thankreport_pagination'] = {
        'count': thanks_paginator.count,
        'pages': thanks_paginator.num_pages,
        'current': thanks.number,
        'is_paginated': thanks_paginator.num_pages > 1
    }

    append_incidents_statistics(context)
    append_thanks_statistics(context)

    context['incidents_locations'] = Report.objects.values('latitude', 'longitude', 'category__definition', 'pk')
    context['thanks_locations'] = ThankReport.objects.values('latitude', 'longitude', 'category__definition', 'pk')

    #context = RequestContext(request, context)
    # context.update(csrf(request))
    return render(request, template_name, context)
    # else:
    # return redirect_to_login(next[, login_url, redirect_field_name])
    # return redirect_to_login('/')
