import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListHybridResponseMixin, DetailHybridResponseMixin
from django import forms

from reports.models import Entry


TEMPLATE_BASE = 'entries'


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        exclude = ('slug',)


class EntryListView(ListView):
    model = Entry
    template_name = TEMPLATE_BASE + '/list.html'


class EntryListHybridView(ListHybridResponseMixin, EntryListView):
    pass


class EntryDetailView(DetailView):
    model = Entry
    template_name = TEMPLATE_BASE + '/view.html'


class EntryDetailHybridView(DetailHybridResponseMixin, EntryDetailView):
    pass


class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm
    template_name = TEMPLATE_BASE + '/new.html'


class EntryUpdateView(UpdateView):
    model = Entry
    template_name = TEMPLATE_BASE + '/edit.html'


class EntryDeleteView(DeleteView):
    model = Entry
    template_name = TEMPLATE_BASE + '/delete.html'
    success_url = '..'
