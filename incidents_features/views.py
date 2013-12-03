import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import PaginatedListHybridResponseMixin, DetailHybridResponseMixin
from django import forms

from incidents.models import Feature


TEMPLATE_BASE = 'incidents_features'


class FeatureForm(forms.ModelForm):

    class Meta:
        model = Feature
        exclude = ('slug',)


class FeatureListView(ListView):
    model = Feature
    template_name = TEMPLATE_BASE + '/list.html'


class FeatureListHybridView(PaginatedListHybridResponseMixin, FeatureListView):
    pass


class FeatureDetailView(DetailView):
    model = Feature
    template_name = TEMPLATE_BASE + '/view.html'


class FeatureDetailHybridView(DetailHybridResponseMixin, FeatureDetailView):
    pass


class FeatureCreateView(CreateView):
    model = Feature
    form_class = FeatureForm
    template_name = TEMPLATE_BASE + '/new.html'


class FeatureUpdateView(UpdateView):
    model = Feature
    template_name = TEMPLATE_BASE + '/edit.html'


class FeatureDeleteView(DeleteView):
    model = Feature
    template_name = TEMPLATE_BASE + '/delete.html'
    success_url = '..'
