from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import CharField
from django.db.models.functions import Cast, Extract
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Prefetch
from django.db.models import Q, Case, When, Value, F
from datetime import datetime, time, timedelta
from constance import config
from .forms import *

# Create your views here.

def main(request):
	return render(request,'main.html',{})

class CreateUserView(CreateView):
	form_class = CreateUserForm
	template_name = 'auth/create_user.html'
	success_url = reverse_lazy('users:list_user')

class ListUserView(ListView):
	model = User
	template_name = 'auth/list_user.html'
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
						'username',
						'first_name',
						'last_name',
						Cast('email', CharField())
					)
				).filter(
					search=search,
					is_staff=False
				).order_by('id')
		else:
			return self.model.objects.all().filter(is_staff=False).order_by('id')

class ConstanceView(FormView):
	template_name = 'constance.html'
	form_class = ConstanceForm
	success_url = '/'
	def form_valid(self, form):
		form.save()
		return super().form_valid(form)

def metricas_inline_view(request, pk):
	instance = get_object_or_404(User, id=pk)
	queryset = Metricas.objects.filter(user=instance)
	fom_inline = metricas_inline
	helper = MetricasHelperForm()
	if request.method == 'POST':
		formset = fom_inline(request.POST, request.FILES, instance=instance)
		if formset.is_valid():
			formset.save()
			if 'add' in request.POST:
				return HttpResponseRedirect(request.path)
			else:
				return HttpResponseRedirect(reverse_lazy('users:list_user'))
	else:
		formset = fom_inline(instance=instance)
	return render(request, 'metricas.html',{'formset':formset, 'helper':helper, 'instance':instance})

class PlanillaDataView(FormView):
	form_class = DateForm
	template_name = 'planillas/planilla_date.html'
	success_url = 'users:planilla_detail'
	def form_valid(self, form):
		return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs={'pk':self.kwargs['pk'],'fini':(form.cleaned_data['inicio']), 'ffin':(form.cleaned_data['fin'])}))

class PlanillaDetail(DetailView):
	model = User
	template_name = 'planillas/planilla_detail.html'
	def get_object(self, query=None):
		asd1 = config.ENTRADA_M_I #datetime.strptime('8:0:0', '%H:%M:%S').time()
		asd2 = config.ENTRADA_M_M #datetime.strptime('8:20:0', '%H:%M:%S').time()

		asd3 = config.SALIDA_M_I #datetime.strptime('12:0:0', '%H:%M:%S').time()
		asd4 = config.SALIDA_M_M #datetime.strptime('13:30:0', '%H:%M:%S').time()
		
		asd5 = config.ENTRADA_T_I #datetime.strptime('14:0:0', '%H:%M:%S').time()
		asd6 = config.ENTRADA_T_M #datetime.strptime('14:20:0', '%H:%M:%S').time()

		asd7 = config.SALIDA_T_I #datetime.strptime('18:0:0', '%H:%M:%S').time()
		asd8 = config.SALIDA_T_M #datetime.strptime('23:0:0', '%H:%M:%S').time()

		late = timedelta(minutes=10)
		#import pdb; pdb.set_trace()
		print((datetime.combine(datetime(1,1,1),asd2) - late).time())
		print(asd2)
		return self.model.objects.prefetch_related(
			Prefetch('tiqueo_set',
				Tiqueo.objects.filter(
					Q(fecha__time__range=(asd1,asd2))|
					Q(fecha__time__range=(asd3,asd4))|
					Q(fecha__time__range=(asd5,asd6))|
					Q(fecha__time__range=(asd7,asd8)),
					fecha__range=(self.kwargs['fini'],self.kwargs['ffin'])
				).annotate(
					minutos_tarde_m= Case(
						When(
							Q(fecha__time__gte=(datetime.combine(datetime(1,1,1),asd2) - late).time(), fecha__time__lt=asd2), 
							then=Extract(F('fecha__time') - (datetime.combine(datetime(1,1,1),asd2) - late).time(),'minute')
						)
					),
					minutos_tarde_t= Case(
						When(
							Q(fecha__time__gte=(datetime.combine(datetime(1,1,1),asd6) - late).time(), fecha__time__lt=asd6),
							then=Extract(F('fecha__time') - (datetime.combine(datetime(1,1,1),asd6) - late).time(),'minute')
						)
					),
				).order_by('fecha')
			)
		).get(id=self.kwargs['pk'])
