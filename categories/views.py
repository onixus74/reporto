from django.shortcuts import render_to_response

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListHybridResponseMixin, DetailHybridResponseMixin

from reports.models import Category


class CategoryListView(ListView):
	model = Category
	template_name = "categories/list.html"


class CategoryListHybridView(ListHybridResponseMixin, CategoryListView):
	pass


class CategoryDetailView(DetailView):
	model = Category
	template_name = "categories/view.html"


class CategoryDetailHybridView(DetailHybridResponseMixin, CategoryDetailView):
	pass


class CategoryCreateView(CreateView):
	model = Category
	template_name = "categories/new.html"


class CategoryUpdateView(UpdateView):
	model = Category
	template_name = "categories/edit.html"


class CategoryDeleteView(DeleteView):
	model = Category
	template_name = "categories/delete.html"
	success_url = '/categories/'


def list_categories(request, *args, **kwargs):
	template_name = "categories/index.html"
	context = {
		"items": Category.objects.all()
	}
	return render_to_response(template_name, context)
