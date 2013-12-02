import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListHybridResponseMixin, DetailHybridResponseMixin
from django import forms

from incidents.models import ThankCategory


TEMPLATE_BASE = 'thanks_categories'


class ThankCategoryForm(forms.ModelForm):

    class Meta:
        model = ThankCategory
        exclude = ('slug',)


class ThankCategoryListView(ListView):
    model = ThankCategory
    template_name = TEMPLATE_BASE + '/list.html'


class ThankCategoryListHybridView(ListHybridResponseMixin, ThankCategoryListView):
    pass


class ThankCategoryDetailView(DetailView):
    model = ThankCategory
    template_name = TEMPLATE_BASE + '/view.html'


class ThankCategoryDetailHybridView(DetailHybridResponseMixin, ThankCategoryDetailView):
    pass


class ThankCategoryCreateView(CreateView):
    model = ThankCategory
    form_class = ThankCategoryForm
    template_name = TEMPLATE_BASE + '/new.html'


class ThankCategoryUpdateView(UpdateView):
    model = ThankCategory
    template_name = TEMPLATE_BASE + '/edit.html'


class ThankCategoryDeleteView(DeleteView):
    model = ThankCategory
    template_name = TEMPLATE_BASE + '/delete.html'
    success_url = '..'
