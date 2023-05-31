from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, DetailView
from apps.users.forms import search_form
from django.urls import reverse_lazy
from .forms import *
from .models import *

# Create your views here.

class ListQuejasView(ListView):
	model = Quejas
	template_name = 'quejas/list_quejas.html'
	form_class = search_form
	paginate_by = 10
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class()
		if self.request.GET:
			context['form'] = self.form_class(self.request.GET)
			form = self.form_class(self.request.GET)
			if form.is_valid():
				if form.cleaned_data['search']=='':
					context['searchdata'] = None
				else:
					context['searchdata'] = form.cleaned_data['search']
		return context
	def get_queryset(self):
		search = None
		if self.request.method == "GET":
			form = self.form_class(self.request.GET)
			if form.is_valid():
				search = form.cleaned_data['search']
		if (search):
			return self.model.objects.annotate(
					search=SearchVector(
						Cast('id', CharField()),
						Cast('queja', CharField())
					)
				).filter(
					search=search,
				).order_by('id')
		else:
			return self.model.objects.all().order_by('id')

class ListQuejasPersonalesView(ListView):
	model = Quejas
	template_name = 'quejas/list_quejas_pesonales.html'
	form_class = search_form
	paginate_by = 10
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class()
		if self.request.GET:
			context['form'] = self.form_class(self.request.GET)
			form = self.form_class(self.request.GET)
			if form.is_valid():
				if form.cleaned_data['search']=='':
					context['searchdata'] = None
				else:
					context['searchdata'] = form.cleaned_data['search']
		return context
	def get_queryset(self):
		search = None
		if self.request.method == "GET":
			form = self.form_class(self.request.GET)
			if form.is_valid():
				search = form.cleaned_data['search']
		if (search):
			return self.model.objects.annotate(
					search=SearchVector(
						Cast('id', CharField()),
						Cast('queja', CharField())
					)
				).filter(
					search=search,
					user=self.request.user
				).order_by('id')
		else:
			return self.model.objects.filter(user=self.request.user).order_by('id')

class QuejasCreateView(CreateView):
	form_class = QuejasForm
	template_name = 'quejas/create_quejas.html'
	success_url = reverse_lazy('empleado:list_quejas_personales')
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class QuejasUpdateView(UpdateView):
	model = Quejas
	form_class = QuejasForm
	template_name = 'quejas/update_quejas.html'
	success_url = reverse_lazy('empleado:list_quejas_personales')

class ListRequerimientoView(ListView):
	model = Requerimiento
	template_name = 'rquerimiento/list_requerimientos_personales.html'
	form_class = search_form
	paginate_by = 10
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'form' not in context:
			context['form'] = self.form_class()
		if self.request.GET:
			context['form'] = self.form_class(self.request.GET)
			form = self.form_class(self.request.GET)
			if form.is_valid():
				if form.cleaned_data['search']=='':
					context['searchdata'] = None
				else:
					context['searchdata'] = form.cleaned_data['search']
		return context
	def get_queryset(self):
		search = None
		if self.request.method == "GET":
			form = self.form_class(self.request.GET)
			if form.is_valid():
				search = form.cleaned_data['search']
		if (search):
			return self.model.objects.annotate(
					search=SearchVector(
						Cast('id', CharField()),
						Cast('requerimiento', CharField())
					)
				).filter(
					search=search,
					user=self.request.user
				).order_by('id')
		else:
			return self.model.objects.filter(user=self.request.user).order_by('id')

class RequerimientoCreateView(CreateView):
	form_class = RequerimientoForm
	template_name = 'rquerimiento/create_requeriminto.html'
	success_url = reverse_lazy('empleado:list_requerimiento_personales')
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class RequerimientoUpdateView(UpdateView):
	model = Requerimiento
	form_class = RequerimientoForm
	template_name = 'rquerimiento/update_requerimiento.html'
	success_url = reverse_lazy('empleado:list_requerimiento_personales')
