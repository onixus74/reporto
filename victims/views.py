import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from base.utils.views import ListHybridResponseMixin, DetailHybridResponseMixin

from reports.models import Victim


class VictimListView(ListView):
	model = Victim
	template_name = "victims/list.html"


class VictimListHybridView(ListHybridResponseMixin, VictimListView):
	pass


class VictimDetailView(DetailView):
	model = Victim
	template_name = "victims/view.html"


class VictimDetailHybridView(DetailHybridResponseMixin, VictimDetailView):
	pass


class VictimCreateView(CreateView):
	model = Victim
	template_name = "victims/new.html"


class VictimUpdateView(UpdateView):
	model = Victim
	template_name = "victims/edit.html"


class VictimDeleteView(DeleteView):
	model = Victim
	template_name = "victims/delete.html"
	success_url = '/victims/'
