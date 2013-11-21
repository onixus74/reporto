import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListHybridResponseMixin, DetailHybridResponseMixin
from django import forms

from reports.models import Feature


class FeatureForm(forms.ModelForm):
	class Meta:
		model = Feature
		exclude = ('slug',)


class FeatureListView(ListView):
	model = Feature
	template_name = "features/list.html"

class FeatureListHybridView(ListHybridResponseMixin, FeatureListView):
	pass

class FeatureDetailView(DetailView):
	model = Feature
	template_name = "features/view.html"


class FeatureDetailHybridView(DetailHybridResponseMixin, FeatureDetailView):
	pass


class FeatureCreateView(CreateView):
	model = Feature
	form_class = FeatureForm
	template_name = "features/new.html"


class FeatureUpdateView(UpdateView):
	model = Feature
	template_name = "features/edit.html"


class FeatureDeleteView(DeleteView):
	model = Feature
	template_name = "features/delete.html"
	success_url = '..'
