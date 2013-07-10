from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from reports.models import Feature


class FeatureListView(ListView):
  model = Feature
  template_name = "features/list.html"


class FeatureDetailView(DetailView):
  model = Feature
  template_name = "features/view.html"


class FeatureCreateView(CreateView):
  model = Feature
  template_name = "features/new.html"


class FeatureUpdateView(UpdateView):
  model = Feature
  template_name = "features/edit.html"


class FeatureDeleteView(DeleteView):
  model = Feature
  template_name = "features/delete.html"
  success_url = '/features/'
