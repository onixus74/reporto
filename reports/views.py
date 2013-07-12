from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def index(request, *args, **kwargs):
	template_name = "reports/index.html"
	context = {
		"object_list": Report.objects.all()
	}
	return render_to_response(template_name, context)


def dashboard(request, *args, **kwargs):
	template_name = "reports/dashboard.html"
	context = {
		"object_list": Report.objects.all()
	}
	return render_to_response(template_name, context)


def submission(request, *args, **kwargs):
	template_name = "reports/submission.html"
	context = {
		"message": "Hello!"
	}
	return render_to_response(template_name, context)


def item(request, id, *args, **kwargs):
  template_name = "reports/view.html"
  context = {
    "object": Report.objects.get(id=id)
  }
  return render_to_response(template_name, context)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from reports.models import Report

class ReportListView(ListView):
  model = Report
  template_name = "reports/list.html"


class ReportDetailView(DetailView):
  model = Report
  template_name = "reports/view.html"


class ReportCreateView(CreateView):
  model = Report
  template_name = "reports/new.html"


class ReportUpdateView(UpdateView):
  model = Report
  template_name = "reports/edit.html"


class ReportDeleteView(DeleteView):
  model = Report
  template_name = "reports/delete.html"
  success_url = '/reports/'
