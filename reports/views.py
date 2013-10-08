import logging
logger = logging.getLogger(__name__)

import uuid
import os
import json
import logging
import shutil
from datetime import datetime, date

from django.conf import settings
from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson

from django import forms
from django.forms.models import model_to_dict
from django.db.models import Count, Min, Sum, Max, Avg
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.base import View
from django.views.generic import FormView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from base.utils.views import JSONResponse, JSONDataView, ListHybridResponseMixin, PaginatedListHybridResponseMixin, DetailHybridResponseMixin, AjaxableResponseMixin

from django.core.files.storage import default_storage

from reports.models import *


def index(request, template_name = "reports/index.html", *args, **kwargs):
	context = {
		"object_list": Report.objects.all()
	}
	return render(request, template_name, context)


class ReportsDashboard(PaginatedListHybridResponseMixin, ListView):
	""" """
	model = Report
	template_name = "reports/dashboard.html"

	def get_context_data(self, **kwargs):
		"""
			Prepare context parameter 'reports_by_category' with the following structure
			reports_by_category = [
				{ 'label': 'Verbal Violence', 'value': 20 },
				{ 'label': 'Violence', 'value': 10 },
				{ 'label': 'Rape', 'value': 20 },
				{ 'label': 'Lack of Investigation and Prosecution', 'value': 50 }
			]
		"""
		context = super(ReportsDashboard, self).get_context_data(**kwargs)

		if self.is_json():

			context['html'] = render_to_string("reports/dashbload_reports_list.html", { 'report_list': context['report_list'] })
			context['report_list'] = None

		else:

			reports_by_category = Report.objects.values('category__definition').annotate(Count("id")).order_by('category__definition')
			context['reports_by_category'] = [ { 'label': i['category__definition'], 'value': i['id__count'] } for i in reports_by_category ]

			victim_gender_display = dict(Victim.GENDER)
			reports_by_victim_gender = Report.objects.values('victim__gender').annotate(Count("id")).order_by('victim__gender')
			context['reports_by_victim_gender'] = [ { 'label': victim_gender_display[i['victim__gender']], 'value': i['id__count'] } for i in reports_by_victim_gender ]

			victim_education_display = dict(Victim.EDUCATION)
			reports_by_victim_education = Report.objects.values('victim__education').annotate(Count("id")).order_by('victim__education')
			context['reports_by_victim_education'] = [ { 'label': victim_education_display[i['victim__education']], 'value': i['id__count'] } for i in reports_by_victim_education ]

			reports_by_feature = Report.objects.values('features__definition').annotate(Count("id")).order_by('features__definition')
			context['reports_by_feature'] = [ { 'label': i['features__definition'], 'count': i['id__count'] } for i in reports_by_feature ]

			reports_by_date = Report.objects.extra({'date' : "date(datetime)"}).values('date').annotate(Count('id')).order_by('date')
			context['reports_by_date'] = [ { 'date': i['date'], 'total': i['id__count'] } for i in reports_by_date ]

			context['categories'] = [ category.__unicode__() for category in Category.objects.all() ]

			for category in Category.objects.all():
				result = Report.objects.extra({'date' : "date(datetime)"}).filter(category=category).values('date').annotate(Count('id')).order_by('date')
				result = [ { 'date': i['date'], category.__unicode__(): i['id__count'] } for i in result ]
				if len(result) > 0:
					context['reports_by_date'] = merge_lists(context['reports_by_date'], result, 'date')

		return context


def merge_lists(l1, l2, key):
	merged = {}
	for item in l1+l2:
		if item[key] in merged:
			merged[item[key]].update(item)
		else:
			merged[item[key]] = item
	return [val for (_, val) in merged.items()]

# def paginated_reports(request, *args, **kwargs):

# 	return JSONResponse({
# 		'success': True,
# 		'exist': exist,
# 		'list': similars,
# 		'html': render_to_string("reports/submit_similar_reports_list.html", { 'reports': similars })
# 	})


class ReportView(DetailHybridResponseMixin, DetailView):
	""" """
	model = Report
	template_name = "reports/view.html"


# def item(request, id, *args, **kwargs):
# 	template_name = "reports/view.html"
# 	context = {
# 		"object": Report.objects.get(id=id)
# 	}
# 	return render(request, template_name, context)


# @csrf_exempt
# class SubmissionForm(forms.Form):
# 	name = forms.CharField('Name', required=True)


# def submission(request, template_name = "reports/submit.html", *args, **kwargs):
# 	form = SubmissionForm(request.POST or None)
# 	#form = SubmissionForm(request.POST or None, request.FILES or None)
# 	if form.is_valid():
# 		logger.debug("form valid")
# 		return redirect("home")
# 	context = {
# 		"message": "Hello!",
# 		"form": form
# 	}
# 	return render(request, template_name, context)


# def submission_json(request, *args, **kwargs):
# 	data = {
# 		"message": "Hello!",
# 	}
# 	return HttpResponse(simplejson.dumps(data), content_type="application/json")



# class ReportSubmissionForm(forms.Form):
# 	class Meta:
# 		model = Report
# 		#fields = [...]


class ReportCreateForm(forms.ModelForm):
	class Meta:
		model = Report
		exclude = ('created_by','victim')


from victims.views import VictimForm as BaseVictimForm

class VictimCreateForm(BaseVictimForm):
	class Meta(BaseVictimForm.Meta):
		exclude = ('user','description')

from users.views import VictimForm as VictimUpdateForm

# class VictimUpdateForm(BaseVictimForm):
# 	class Meta(BaseVictimForm.Meta):
# 		exclude = ('user','firstname','lastname','email','description')


def report_submit(request, template_name = "reports/submit.html", *args, **kwargs):
	logger.debug('POST %s', request.POST)
	logger.debug('FILES %s', request.FILES)

	context = {}
	form = ReportCreateForm(request.POST or None, request.FILES or None)
	context['form'] = form

	victim_form = VictimCreateForm(request.POST or None, prefix = 'victim')
	context['victim_form'] = victim_form

	try:
		victim = Victim.objects.get(user=request.user)
	except Victim.DoesNotExist:
		victim = None
	victim_profile_form = VictimUpdateForm(request.POST or None, instance = victim, prefix = 'reporter-victim')
	context['victim_profile_form'] = victim_profile_form

	if request.method == 'GET':
		# create report submit id for files upload
		rsid = uuid.uuid1().hex
		#RSIDs = request.session.get('RSIDs', [])
		#RSIDs.append(rsid)
		#request.session['RSIDs'] = RSIDs
		context['report_submit_id'] = rsid
		#victims = Victim.objects.all()
		#context['victims'] = victims
		reports = Report.objects.all()[:9]
		context['reports'] = reports

	victim_id = request.POST.get('victim', None)
	logger.debug('VICTIM %s', victim_id)

	if form.is_valid() and (
		   (victim_id != '0' and victim_id != 'user')
		or (victim_id == '0' and victim_form.is_valid())
		or (victim_id == 'user' and victim_profile_form.is_valid())
	):

		if victim_id == 'user': # the user is the victim
			try:
				victim = Victim.objects.get(user=request.user)
				# update goes here!
			except Victim.DoesNotExist:
				#victim = Victim(category=victim_profile_form.instance.category, firstname=request.user.first_name, lastname=request.user.last_name, gender=victim_profile_form.instance.gender, email=request.user.email, user=request.user);
				#victim.save();
				pass
			victim_profile_form.instance.firstname = request.user.first_name
			victim_profile_form.instance.lastname = request.user.last_name
			victim_profile_form.instance.email = request.user.email
			victim_profile_form.instance.user = request.user
			victim = victim_profile_form.save()
		elif victim_id != '0': # existent victim
			victim = Victim.objects.get(pk=victim_id)
		else: # create new user
			victim = victim_form.save()

		logger.debug('VICTIM %s', victim)

		#victim = victim_form.save()
		form.instance.victim = victim
		form.instance.created_by = request.user
		if request.user.is_moderator():
			form.instance.is_verified = True
		report = form.save()

		files = request.FILES.getlist('files[]')
		logger.debug('FILES %s', files)

		#media_path = os.path.join('reports', str(report.pk))
		#logger.debug('MEDIA PATH %s', media_path)

		logger.debug('OBJECT %s', report)

		for f in files:
			logger.debug('FILE %s', f)
			report.media.create(file=f)
			#file_path = os.path.join(media_path, f.name)
			#logger.debug('FILE PATH %s', file_path)
			#file_path = default_storage.save(file_path, f)
			#report.media.create(url=file_path)

		report.save()

		if request.is_ajax():
			return JSONResponse({
				'success': True,
				'object': report,
				'url': report.get_absolute_url(),
				'notification': { 'title': "Adding Report", 'body': "Report added." }
			})
		else:
			return redirect(report.get_absolute_url())

	else:
		if request.is_ajax():
			if victim_id == 'user':
				form.errors['victim'] = victim_profile_form.errors
			elif victim_id == '0':
				form.errors['victim'] = victim_form.errors
			return JSONResponse({
				'success': False,
				'errors': form.errors,
				'notification': { 'title': "Adding Report", 'body': form.errors.get('__all__', None) or form.errors.as_ul() or "Failed to add a report" }
			}, status=400)

	return render(request, template_name, context)


# class SimilarReportForm(forms.ModelForm):
# 	class Meta:
# 		model = Report
# 		fields = ('category', 'location', 'datetime')


# class SimilarInputForm(forms.Form):
# 	category = forms.CharField()
# 	location = forms.CharField()
# 	datetime = forms.CharField()
# 	date = forms.CharField()
# 	victim_firstname = forms.CharField()
# 	victim_lastname = forms.CharField()


def similar_reports(request, *args, **kwargs):
	logger.debug('POST %s', request.POST)

	if request.method == 'POST':
		pass

	similars = []

	reports = Report.objects.all()

	# category = request.POST.get('category', None);
	# if category:
	# 	reports = reports.filter(category=category)

	input_category = request.POST.get('category', '');
	if len(input_category) == 0:
		 input_category = None

	input_location = request.POST.get('location', '');
	if len(input_location) == 0:
		input_location = None

	input_datetime = request.POST.get('date', '');
	if len(input_datetime) == 0:
		input_datetime = None

	input_victim_firstname = request.POST.get('victim-firstname', '');
	if len(input_victim_firstname) == 0:
		 input_victim_firstname = None

	input_victim_lastname = request.POST.get('victim-lastname', '');
	if len(input_victim_lastname) == 0:
		  input_victim_lastname = None

	logger.debug('CATEGORY %s', input_category)
	logger.debug('DATETIME %s', input_datetime)
	logger.debug('VICTIM FIRSTNAME %s', input_victim_firstname)
	logger.debug('VICTIM LASTNAME %s', input_victim_lastname)

	for report in reports:
		#similarity_value = 0
		similarities = []

		#logger.debug('CATEGORY %s', [input_category, report.category])
		if input_category and int(input_category) == report.category.id:
			similarities.append('category')

		#logger.debug('DATATIME %s', [input_datetime, report.datetime])
		if input_datetime and datetime.strptime(input_datetime, '%Y-%m-%d').date() == report.datetime.date():
			similarities.append('datetime')

		#logger.debug('LOCATION %s', [input_location, report.location])
		if input_location:
			lat1, lan1 = map(float, input_location.split(','))
			lat2, lan2 = map(float, report.location.split(','))
			distance = locations_distance(lat1, lan1, lat2, lan2)
			#logger.debug('LOCATION %s', distance)
			#if input_location and input_location == report.location:
			if input_location and distance < 10: # distance lower than 10km
				similarities.append('location')

		#logger.debug('VICTIM %s', [input_victim_firstname, input_victim_lastname, report.victim])
		if input_victim_firstname and input_victim_lastname:
			input_victim_fullname = ("%s %s" % (input_victim_firstname, input_victim_lastname)).strip()
			if string_distance(input_victim_fullname, report.victim.get_fullname()) > 0.8: # similar string values
				similarities.append('victim')

		report.similarities = similarities
		report.similarity = len(similarities)

		if report.similarity > 0:
			#report.similarities = similarities
			similars.append(report)
			#similars_meta.append(similarities)

	exist = len(similars) > 0

	similars = sorted(similars, key=lambda report: report.similarity, reverse=True)[:9]

	return JSONResponse({
		'success': True,
		'exist': exist,
		'list': similars,
		'html': render_to_string("reports/submit_similar_reports_list.html", { 'reports': similars })
	})

from math import radians, cos, sin, asin, sqrt

def locations_distance(lon1, lat1, lon2, lat2):
	"""
	Calculate the great circle distance between two points  on the earth (specified in decimal degrees)
	"""
	# convert decimal degrees to radians
	lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
	# haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	km = 6367 * c
	return km

import difflib

def string_distance(str1, str2):
    return difflib.SequenceMatcher(a=str1.lower(), b=str2.lower()).ratio()

# class ReportSubmitView(AjaxableResponseMixin, CreateView):
# 	""" """
# 	model = Report
# 	form_class = ReportCreateForm
# 	template_name = "reports/submit.html"

# 	def get_context_data(self, **kwargs):
# 		logger.debug(kwargs)

# 		# create report submit id for files upload
# 		rsid = uuid.uuid1().hex
# 		#RSIDs = self.request.session.get('RSIDs', [])
# 		#RSIDs.append(rsid)
# 		#self.request.session['RSIDs'] = RSIDs
# 		kwargs['report_submit_id'] = rsid
# 		kwargs['victim_form'] = VictimCreateForm(prefix = 'victim')
# 		kwargs['victims'] = Victim.objects.all()
# 		kwargs['reports'] = Report.objects.all()

# 		logger.debug(kwargs)
# 		return kwargs

# 	#def form_invalid(self, form):

# 	def form_valid(self, form):
# 		logger.debug('POST %s', self.request.POST)
# 		logger.debug('FILES %s', self.request.FILES)

# 		victim = self.request.POST['victim']
# 		logger.debug('VICTIM %s', victim)

# 		if victim == 'user':
# 			# the user is the victim
# 			victim = Victim.objects.get(user=self.request.user)
# 		elif victim != '0':
# 			# existent victim
# 			victim = Victim.objects.get(pk=victim)
# 		else:
# 			# create new user
# 			victimForm = VictimCreateForm(self.request.POST, prefix = 'victim')
# 			if victimForm.is_valid():
# 				victim = victimForm.save()
# 			else:
# 				form = super(ReportSubmitView, self).form_invalid(victimForm)
# 				logger.debug('FORM VICTIM INVALID %s %s', form, victimForm)
# 				return form

# 		logger.debug('VICTIM %s', victim)

# 		form.instance.victim = victim

# 		form.instance.created_by = self.request.user

# 		form = super(ReportSubmitView, self).form_valid(form)

# 		#logger.debug('FORM %s', form.instance)

# 		logger.debug('REPORT %s', self.object.pk)

# 		files = self.request.FILES.getlist('files[]')
# 		logger.debug('FILES %s', files)

# 		media_path = os.path.join('reports', str(self.object.pk))
# 		logger.debug('MEDIA PATH %s', media_path)

# 		logger.debug('OBJECT %s', self.object)

# 		for f in files:
# 			logger.debug('FILE %s', f)
# 			#self.object.media.create(file=f)
# 			file_path = os.path.join(media_path, f.name)
# 			logger.debug('FILE PATH %s', file_path)
# 			file_path = default_storage.save(file_path, f)
# 			self.object.media.create(url=file_path)
# 			#media = Media(url=file_path)
# 			#self.object.media.add(media)

# 		self.object.save()

# 		# report_submit_id = self.request.POST['rsid']
# 		# #report_submit_id in request.session.get('RSIDs', [])
# 		# logger.debug(report_submit_id)

# 		# media_path = os.path.join('reports', 'tmp', report_submit_id)
# 		# logger.debug(media_path)

# 		# #media_files_key = 'report_submit_' + report_submit_id + '_files'
# 		# #media_files = self.request.session.get(media_files_key, [])
# 		# #logger.debug(media_files)

# 		# persistant_media_path = os.path.join('reports', str(self.object.pk))
# 		# logger.debug(persistant_media_path)

# 		# if default_storage.exists(media_path):
# 		# 	shutil.move(default_storage.path(media_path), default_storage.path(persistant_media_path))

# 		return form


# class MediaForm(forms.ModelForm):
# 	class Meta:
# 		model = Media

# class UploadFileForm(forms.Form):
# 	file = forms.FileField()


# def submit_upload(request, *args, **kwargs):

# 	#logger.debug(request.session.items())
# 	#logger.debug(request.method)
# 	#logger.debug(request.body)
# 	#logger.debug(request.META['CONTENT_TYPE'])
# 	#logger.debug(request.COOKIES)
# 	#logger.debug(request.REQUEST)
# 	#logger.debug(request.GET)
# 	#logger.debug(request.POST)
# 	#logger.debug(request.FILES)

# 	#logger.debug("condition:")
# 	#logger.debug(request.META.has_key('HTTP_X_RSID'))
# 	#logger.debug(request.META['HTTP_X_RSID'])
# 	#logger.debug(request.session.get('RSIDs', None))
# 	#logger.debug(request.META['HTTP_X_RSID'] in request.session.get('RSIDs', []))

# 	if request.method == 'POST' and request.META.has_key('HTTP_X_RSID'):
# 		#and request.META['HTTP_X_RSID'] in request.session.get('RSIDs', []):

# 		report_submit_id = request.META['HTTP_X_RSID']
# 		logger.debug(report_submit_id)

# 		media_path = os.path.join('reports', 'tmp', report_submit_id)
# 		logger.debug(media_path)

# 		#media_files_key = 'report_submit_' + report_submit_id + '_files'
# 		#media_files = request.session.get(media_files_key, [])
# 		#logger.debug(media_files)

# 		files = request.FILES.getlist('files[]')
# 		logger.debug(files)

# 		for f in files:
# 			logger.debug(f)
# 			file_path = os.path.join(media_path, f.name)
# 			logger.debug(file_path)
# 			#media_files.append(file_path)
# 			default_storage.save(file_path, f)

# 		#logger.debug(media_files)

# 		#request.session[media_files_key] = media_files

# 		return JSONResponse({'success': True})

# 	return JSONResponse({'success': False}, status=400)



# class ReportVerifyView(View):
# 	http_method_names = ['get', 'post']

# 	def get(self, request, pk, *args, **kwargs):
# 		report = Report.objects.get(pk=pk)
# 		return JSONResponse({'success': True, 'verified': report.is_verified})

# 	def post(self, request, pk, *args, **kwargs):
# 		report = Report.objects.get(pk=pk)
# 		report.is_verified = True
# 		report.save()
# 		return JSONResponse({'success': True, 'verified': report.is_verified})


def report_verify(request, pk, *args, **kwargs):
	logger.debug('POST %s', request.POST)
	report = Report.objects.get(pk=pk)
	if request.method == 'POST':
		report.is_verified = True
		report.save()
	return JSONResponse({'success': True, 'verified': report.is_verified})


def report_close(request, pk, *args, **kwargs):
	logger.debug('POST %s', request.POST)
	report = Report.objects.get(pk=pk)
	if request.method == 'POST':
		report.is_closed = True
		report.save()
	return JSONResponse({'success': True, 'closed': report.is_closed})


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ('created_by')


def report_comment(request, pk, *args, **kwargs):
	logger.debug('POST %s', request.POST)
	logger.debug('FILES %s', request.FILES)
	form = CommentForm(request.POST or None, request.FILES or None)
	# logger.debug('form.instance.type %s', form.instance.type)
	# if not form.instance.type:
	# 	form.instance.type = Comment.UPDATE
	# logger.debug('form.instance.type %s', form.instance.type)

	if form.is_valid():
		form.instance.created_by = request.user
		comment = form.save()
		report = Report.objects.get(pk=pk)
		#comment.report = report
		report.comments.add(comment)
		return JSONResponse({
			'success': True,
			'object': comment,
			'html': render_to_string("reports/view_comment.html", {'comment': comment}),
			'notification': { 'title': "Adding Comment", 'body': "Comment added." }
		})
	else:
		return JSONResponse({
			'success': False,
			'errors': form.errors,
			#'notification': { 'title': "Adding Comment", 'body': "Failed to add comment" }
			#'notification': { 'title': "Adding Comment", 'body': form.errors.get('__all__', None) or "<br>".join(["<br>".join(errors) for (field,errors) in form.errors.items()]) }
			'notification': { 'title': "Adding Comment", 'body': form.errors.get('__all__', None) or form.errors.as_ul() or "Failed to add comment" }
		}, status=400)


def stats_xxx(request, *args, **kwargs):
	#data = Report.objects.get() # data request
	response = {
	 #'reports': data,
	 'Verbal Vilence': 15,
	 'Vilance': 10,
	}
	return JSONResponse(response)




# CRUD


from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListHybridResponseMixin, DetailHybridResponseMixin


class ReportForm(forms.ModelForm):
	class Meta:
		model = Report
		exclude = ('comments','media','created_by')


class ReportListView(ListView):
	model = Report
	template_name = "reports/crud/list.html"


class ReportListHybridView(ListHybridResponseMixin, ReportListView):
	pass


class ReportDetailView(DetailView):
	model = Report
	template_name = "reports/crud/view.html"


class ReportDetailHybridView(DetailHybridResponseMixin, ReportDetailView):
	pass


class ReportCreateView(CreateView):
	model = Report
	form_class = ReportForm
	template_name = "reports/crud/new.html"


class ReportUpdateView(UpdateView):
	model = Report
	form_class = ReportForm
	template_name = "reports/crud/edit.html"


class ReportDeleteView(DeleteView):
	model = Report
	template_name = "reports/crud/delete.html"
	success_url = '/reports/crud/'

