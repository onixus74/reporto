import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import PaginatedListHybridResponseMixin, DetailHybridResponseMixin
from django import forms

from incidents.models import Victim


TEMPLATE_BASE = 'incidents_victims'


class VictimForm(forms.ModelForm):

    class Meta:
        model = Victim
        widgets = {
            'category': forms.RadioSelect(),
            'gender': forms.RadioSelect(),
        }


class VictimListView(ListView):
    model = Victim
    template_name = TEMPLATE_BASE + '/list.html'


class VictimListHybridView(PaginatedListHybridResponseMixin, VictimListView):
    pass


class VictimDetailView(DetailView):
    model = Victim
    template_name = TEMPLATE_BASE + '/view.html'


class VictimDetailHybridView(DetailHybridResponseMixin, VictimDetailView):
    pass


class VictimCreateView(CreateView):
    model = Victim
    form_class = VictimForm
    template_name = TEMPLATE_BASE + '/new.html'


class VictimUpdateView(UpdateView):
    model = Victim
    form_class = VictimForm
    template_name = TEMPLATE_BASE + '/edit.html'


class VictimDeleteView(DeleteView):
    model = Victim
    template_name = TEMPLATE_BASE + '/delete.html'
    success_url = '..'
