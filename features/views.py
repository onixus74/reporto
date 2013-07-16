from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListMultiResponseMixin, DetailMultiResponseMixin

from reports.models import Feature


class FeatureListView(ListView):
	model = Feature
	template_name = "features/list.html"

class FeatureListMultiView(ListMultiResponseMixin, FeatureListView):
	pass

class FeatureDetailView(DetailView):
	model = Feature
	template_name = "features/view.html"


class FeatureDetailMultiView(DetailMultiResponseMixin, FeatureDetailView):
	pass


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
