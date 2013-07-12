from django.shortcuts import render_to_response
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from reports.models import Victim


class VictimListView(ListView):
  model = Victim
  template_name = "victims/list.html"


class VictimDetailView(DetailView):
  model = Victim
  template_name = "victims/view.html"


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
