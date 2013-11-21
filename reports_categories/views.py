import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListHybridResponseMixin, DetailHybridResponseMixin
from django import forms

from reports.models import Category


TEMPLATE_BASE = 'reports_categories'


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        exclude = ('slug',)


class CategoryListView(ListView):
    model = Category
    template_name = TEMPLATE_BASE + '/list.html'


class CategoryListHybridView(ListHybridResponseMixin, CategoryListView):
    pass


class CategoryDetailView(DetailView):
    model = Category
    template_name = TEMPLATE_BASE + '/view.html'


class CategoryDetailHybridView(DetailHybridResponseMixin, CategoryDetailView):
    pass


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = TEMPLATE_BASE + '/new.html'


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = TEMPLATE_BASE + '/edit.html'


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = TEMPLATE_BASE + '/delete.html'
    success_url = '..'
