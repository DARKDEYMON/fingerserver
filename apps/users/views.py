from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import CharField
from django.db.models.functions import Cast, Extract
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Prefetch
from django.db.models import Q, Case, When, Value, F, Subquery, OuterRef
from datetime import datetime, time, timedelta
from constance import config
from django.utils.timezone import get_current_timezone
from django_weasyprint import WeasyTemplateResponseMixin
from .forms import *
from .templatetags.transformers import *

# Create your views here.

def main(request):
	return render(request,'main.html',{})

class CreateKardexView(CreateView):
	form_class = KardexForm
	template_name = 'auth/kardex.html'
	success_url = reverse_lazy('users:list_user')
	def form_valid(self, form):
		form.instance.user = User.objects.get(id=self.kwargs['pk'])
		return super().form_valid(form)

class UpdateKardexView(UpdateView):
	model = Kardex
	form_class = KardexForm
	template_name = 'auth/kardex.html'
	success_url = reverse_lazy('users:list_user')

def create_or_update_kardex(request, pk):
	user = User.objects.get(id=pk)
	#import pdb; pdb.set_trace()
	try:
		user.kardex
		return HttpResponseRedirect(reverse_lazy('users:update_kardex', kwargs={'pk':user.kardex.pk}))
	except Exception as e:
		return HttpResponseRedirect(reverse_lazy('users:create_kardex', kwargs={'pk':pk}))

class CreateUserView(CreateView):
	form_class = CreateUserForm
	template_name = 'auth/create_user.html'
	success_url = reverse_lazy('users:list_user')

class UpdateUserView(UpdateView):
	model = User
	form_class = UpdateUserForm
	template_name = 'auth/update_user.html'
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
	template_name = 'planillas/planilla_detail_reporte.html'
	def get_object(self, query=None):
		asd1 = config.ENTRADA_M_I #datetime.strptime('8:0:0', '%H:%M:%S').time()
		asd2 = config.ENTRADA_M_M #datetime.strptime('8:20:0', '%H:%M:%S').time()

		asd3 = config.SALIDA_M_I #datetime.strptime('12:0:0', '%H:%M:%S').time()
		asd4 = config.SALIDA_M_M #datetime.strptime('13:30:0', '%H:%M:%S').time()
		
		asd5 = config.ENTRADA_T_I #datetime.strptime('14:0:0', '%H:%M:%S').time()
		asd6 = config.ENTRADA_T_M #datetime.strptime('14:20:0', '%H:%M:%S').time()

		asd7 = config.SALIDA_T_I #datetime.strptime('18:0:0', '%H:%M:%S').time()
		asd8 = config.SALIDA_T_M #datetime.strptime('23:0:0', '%H:%M:%S').time()

		late = timedelta(minutes=config.TOLERANCIA)
		#import pdb; pdb.set_trace()
		#print((datetime.combine(datetime(1,1,1),asd2) - late).time())
		#print(asd2)
		sub1 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd1,asd2), user__id=self.kwargs['pk']).values('id').order_by('fecha')[:1])
		sub2 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd3,asd4), user__id=self.kwargs['pk']).values('id').order_by('-fecha')[:1])
		sub3 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd5,asd6), user__id=self.kwargs['pk']).values('id').order_by('fecha')[:1])
		sub4 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd7,asd8), user__id=self.kwargs['pk']).values('id').order_by('-fecha')[:1])
		query = self.model.objects.prefetch_related(
			Prefetch('tiqueo_set',
				Tiqueo.objects.filter(
					Q(id__in = [sub1])|
					Q(id__in = [sub2])|
					Q(id__in = [sub3])|
					Q(id__in = [sub4]),
					fecha__date__range=(self.kwargs['fini'],self.kwargs['ffin'])
				).annotate(
					minutos_tarde_m= Case(
						When(
							Q(fecha__time__gte=(datetime.combine(datetime(1,1,1),asd2) - late).time(), fecha__time__lt=asd2), 
							then=Extract(F('fecha__time') - (datetime.combine(datetime(1,1,1),asd2) - late).time(),'minute')
						),
						default=Value(0)
					),
					minutos_tarde_t= Case(
						When(
							Q(fecha__time__gte=(datetime.combine(datetime(1,1,1),asd6) - late).time(), fecha__time__lt=asd6),
							then=Extract(F('fecha__time') - (datetime.combine(datetime(1,1,1),asd6) - late).time(),'minute')
						),
						default=Value(0)
					),
					tipo_entrada= Case(
						When(
							Q(fecha__time__range=(asd1,asd2)),
							then=Value(1),
						),
						When(
							Q(fecha__time__range=(asd3,asd4)),
							then=Value(2),
						),
						When(
							Q(fecha__time__range=(asd5,asd6)),
							then=Value(3),
						),
						When(
							Q(fecha__time__range=(asd7,asd8)),
							then=Value(4),
						)
					),
					
					#t1= Case(
					#	When(
					#		Q(id__in=[sub1])& Q(id__in = [sub2]),
					#		then=Value(True),
					#	),
					#	default=Value(False)
					#),
					#t2= Case(
					#	When(
					#		Q(id__in = [sub3]) & Q(id__in = [sub4]),
					#		then=Value(True),
					#	),
					#	default=Value(False)
					#),

				).order_by('fecha')
			)
		).get(id=self.kwargs['pk'])

		tiqueo = query.tiqueo_set.all()
		#print(tiqueo)

		perg = PermisosGenerales.objects.all()
		permp = Permisos.objects.filter(user__id=self.kwargs['pk'])

		dates = []
		days = (self.kwargs['ffin'] - self.kwargs['fini']).days + 1
		for d in range(days):
			date = self.kwargs['fini'] + timedelta(days = d)
			dates.append(date)

		estado_final = []
		for d in dates:
			dictc = {}
			res = [t for t in tiqueo if t.fecha.astimezone(get_current_timezone()).date() == d]
			tipos = []
			for r in res:
				tipos.append(r.tipo_entrada)
			"""
			if res:
				print(d, res)
			else:
				print(d, 'no vino')
			"""
			dictc['fecha']= d
			dictc['tiqueo'] = res
			dictc['t1'] = set([1,2]).issubset(set(tipos))
			dictc['t2'] = set([3,4]).issubset(set(tipos))
			dictc['fopg'] = permiso1(perg, d)
			dictc['fopp'] = permiso_personal1(permp, d)
			dictc['feriado'] = feriado1(d)
			#import pdb; pdb.set_trace()
			print(dictc)
			estado_final.append(dictc)

		horas = 0
		for hh in estado_final:
			#import pdb; pdb.set_trace()
			if(hh['fopg'] or hh['fopp'] or hh['feriado']):
				horas=horas+8
				continue

			if(hh['t1'] and hh['t2']):
				horas=horas+8
			elif(hh['t1'] or hh['t2']):
				horas=horas+4
		#print(estado_final)
		return {'query': query, 'estado_final': estado_final, 'horas':horas}

class PlanillaDetailPDF(WeasyTemplateResponseMixin, PlanillaDetail):
	pass

class PlanillaDataHCView(FormView):
	form_class = DateForm
	template_name = 'planillas/planilla_date.html'
	success_url = 'users:planilla_detailhc'
	def form_valid(self, form):
		return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs={'pk':self.kwargs['pk'],'fini':(form.cleaned_data['inicio']), 'ffin':(form.cleaned_data['fin'])}))

class PlanillaDetailHC(DetailView):
	model = User
	template_name = 'planillas/planilla_detailhc_reporte.html'
	def get_object(self, query=None):
		asd1 = config.ENTRADA_HC_M_I #datetime.strptime('8:0:0', '%H:%M:%S').time()
		asd2 = config.ENTRADA_HC_M_M #datetime.strptime('8:20:0', '%H:%M:%S').time()

		asd3 = config.SALIDA_HC_T_I #datetime.strptime('12:0:0', '%H:%M:%S').time()
		asd4 = config.SALIDA_HC_T_M #datetime.strptime('13:30:0', '%H:%M:%S').time()

		late = timedelta(minutes=config.TOLERANCIA)
		#import pdb; pdb.set_trace()
		#print((datetime.combine(datetime(1,1,1),asd2) - late).time())
		#print(asd2)
		sub1 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd1,asd2), user__id=self.kwargs['pk']).values('id').order_by('fecha')[:1])
		sub2 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd3,asd4), user__id=self.kwargs['pk']).values('id').order_by('-fecha')[:1])
		query = self.model.objects.prefetch_related(
			Prefetch('tiqueo_set',
				Tiqueo.objects.filter(
					Q(id__in = [sub1])|
					Q(id__in = [sub2]),
					fecha__date__range=(self.kwargs['fini'],self.kwargs['ffin'])
				).annotate(
					minutos_tarde_m= Case(
						When(
							Q(fecha__time__range=((datetime.combine(datetime(1,1,1),asd2) - late).time(), asd2)), 
							then=Extract(F('fecha__time') - (datetime.combine(datetime(1,1,1),asd2) - late).time(),'minute')
						),
						default=Value(0)
					),
					tipo_entrada= Case(
						When(
							Q(fecha__time__range=(asd1,asd2)),
							then=Value(1),
						),
						When(
							Q(fecha__time__range=(asd3,asd4)),
							then=Value(2),
						)
					),
				).order_by('fecha')
			)
		).get(id=self.kwargs['pk'])

		tiqueo = query.tiqueo_set.all()
		#print(tiqueo)

		dates = []
		days = (self.kwargs['ffin'] - self.kwargs['fini']).days + 1
		for d in range(days):
			date = self.kwargs['fini'] + timedelta(days = d)
			dates.append(date)

		estado_final = []
		for d in dates:
			dictc = {}
			res = [t for t in tiqueo if t.fecha.astimezone(get_current_timezone()).date() == d]
			"""
			if res:
				print(d, res)
			else:
				print(d, 'no vino')
			"""
			dictc['fecha']= d
			dictc['tiqueo'] = res
			estado_final.append(dictc)
		#print(estado_final)
		return {'query': query, 'estado_final': estado_final}

class PlanillaDetailHCPDF(WeasyTemplateResponseMixin, PlanillaDetailHC):
	pass

class ListPermisosGView(ListView):
	model = PermisosGenerales
	template_name = 'permisosg/list_permisosg.html'
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
						'motivo',
					)
				).filter(
					search=search,
				).order_by('id')
		else:
			return self.model.objects.all().filter().order_by('id')

class CreatePermisosGView(CreateView):
	form_class = PermisosGeneralesForm
	template_name = 'permisosg/create_permisosg.html'
	success_url = reverse_lazy('users:list_permisosg')

class UpdatePermisosGView(UpdateView):
	model = PermisosGenerales
	form_class = PermisosGeneralesForm
	template_name = 'permisosg/update_permisosg.html'
	success_url = reverse_lazy('users:list_permisosg')

class ListPermisosView(ListView):
	model = Permisos
	template_name = 'permisos/list_permisos.html'
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
						'motivo',
					)
				).filter(
					user__id=self.kwargs['pk'],
					search=search,
				).order_by('id')
		else:
			return self.model.objects.filter(user__id=self.kwargs['pk']).order_by('id')


class CreatePermisosView(CreateView):
	form_class = PermisosForm
	template_name = 'permisos/create_permisos.html'
	success_url = 'users:list_permisos'
	def form_valid(self, form):
		form.instance.user = User.objects.get(id=self.kwargs['pk'])
		return super().form_valid(form)
	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs={'pk': self.object.user_id})

class UpdatePermisosView(UpdateView):
	model = Permisos
	form_class = PermisosForm
	template_name = 'permisos/update_permisos.html'
	success_url = 'users:list_permisos'
	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs={'pk': self.object.user_id})

class PermisosSistemaView(FormView):
	model = User
	model_permissions = Kardex
	form_class = AddPermissionsForm
	template_name = 'permisos_sistema.html'
	success_url = reverse_lazy('users:list_user')
	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['model_permissions'] = self.model_permissions
		return kwargs
	def get_initial(self):
		pk = self.kwargs.get('pk',0)
		self.user = self.model.objects.get(id=pk)
		self.object = self.user
		content_type = ContentType.objects.get_for_model(self.model_permissions)
		permisos_actuales = self.user.user_permissions.filter(content_type=content_type)
		perms = {}
		for p in permisos_actuales:
			perms[p.codename] = True
		return perms
		#return { 'usuarios': True, 'academico': False }
	def form_valid(self, form):
		if form.is_valid():
			data = form.cleaned_data
			for p in data:
				content_type=ContentType.objects.get_for_model(self.model_permissions)
				permission = Permission.objects.get(content_type=content_type, codename=p)
				if data[p]:
					self.user.user_permissions.add(permission)
				else:
					self.user.user_permissions.remove(permission)
		return super().form_valid(form)

class ContratoUser(DetailView):
	model = User
	template_name = 'contrato.html'

class ContratoPDF(WeasyTemplateResponseMixin, ContratoUser):
	pass

class KardexUser(DetailView):
	model = User
	template_name = 'kardex.html'
	def get_context_data(self,**kwargs):
		instance = super().get_context_data(**kwargs)

		asd1 = config.ENTRADA_M_I #datetime.strptime('8:0:0', '%H:%M:%S').time()
		asd2 = config.ENTRADA_M_M #datetime.strptime('8:20:0', '%H:%M:%S').time()

		asd3 = config.SALIDA_M_I #datetime.strptime('12:0:0', '%H:%M:%S').time()
		asd4 = config.SALIDA_M_M #datetime.strptime('13:30:0', '%H:%M:%S').time()
		
		asd5 = config.ENTRADA_T_I #datetime.strptime('14:0:0', '%H:%M:%S').time()
		asd6 = config.ENTRADA_T_M #datetime.strptime('14:20:0', '%H:%M:%S').time()

		asd7 = config.SALIDA_T_I #datetime.strptime('18:0:0', '%H:%M:%S').time()
		asd8 = config.SALIDA_T_M #datetime.strptime('23:0:0', '%H:%M:%S').time()

		late = timedelta(minutes=config.TOLERANCIA)
		#import pdb; pdb.set_trace()
		#print((datetime.combine(datetime(1,1,1),asd2) - late).time())
		#print(asd2)
		sub1 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd1,asd2), user__id=self.kwargs['pk']).values('id').order_by('fecha')[:1])
		sub2 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd3,asd4), user__id=self.kwargs['pk']).values('id').order_by('-fecha')[:1])
		sub3 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd5,asd6), user__id=self.kwargs['pk']).values('id').order_by('fecha')[:1])
		sub4 = Subquery(Tiqueo.objects.filter(fecha__date=OuterRef('fecha__date'),fecha__time__range=(asd7,asd8), user__id=self.kwargs['pk']).values('id').order_by('-fecha')[:1])
		query = self.model.objects.prefetch_related(
			Prefetch('tiqueo_set',
				Tiqueo.objects.filter(
					Q(id__in = [sub1])|
					Q(id__in = [sub2])|
					Q(id__in = [sub3])|
					Q(id__in = [sub4]),
				).annotate(
					minutos_tarde_m= Case(
						When(
							Q(fecha__time__gte=(datetime.combine(datetime(1,1,1),asd2) - late).time(), fecha__time__lt=asd2), 
							then=Extract(F('fecha__time') - (datetime.combine(datetime(1,1,1),asd2) - late).time(),'minute')
						),
						default=Value(0)
					),
					minutos_tarde_t= Case(
						When(
							Q(fecha__time__gte=(datetime.combine(datetime(1,1,1),asd6) - late).time(), fecha__time__lt=asd6),
							then=Extract(F('fecha__time') - (datetime.combine(datetime(1,1,1),asd6) - late).time(),'minute')
						),
						default=Value(0)
					),
					tipo_entrada= Case(
						When(
							Q(fecha__time__range=(asd1,asd2)),
							then=Value(1),
						),
						When(
							Q(fecha__time__range=(asd3,asd4)),
							then=Value(2),
						),
						When(
							Q(fecha__time__range=(asd5,asd6)),
							then=Value(3),
						),
						When(
							Q(fecha__time__range=(asd7,asd8)),
							then=Value(4),
						)
					),
					
					#t1= Case(
					#	When(
					#		Q(id__in=[sub1])& Q(id__in = [sub2]),
					#		then=Value(True),
					#	),
					#	default=Value(False)
					#),
					#t2= Case(
					#	When(
					#		Q(id__in = [sub3]) & Q(id__in = [sub4]),
					#		then=Value(True),
					#	),
					#	default=Value(False)
					#),

				).order_by('fecha')
			)
		).get(id=self.kwargs['pk'])

		tiqueo = query.tiqueo_set.all()
		#print(tiqueo)

		perg = PermisosGenerales.objects.all()
		permp = Permisos.objects.filter(user__id=self.kwargs['pk'])

		dates = []

		
		now = datetime.now(get_current_timezone())
		#import pdb; pdb.set_trace()

		minimo = min(t.fecha for t in tiqueo).date()
		maximo = max(t.fecha for t in tiqueo if t.fecha < now).date()

		print(minimo)
		print(maximo)
		days = (maximo - minimo).days + 1
		for d in range(days):
			date = minimo + timedelta(days = d)
			dates.append(date)

		print(dates)
		estado_final = []
		for d in dates:
			dictc = {}
			res = [t for t in tiqueo if t.fecha.astimezone(get_current_timezone()).date() == d]
			tipos = []
			for r in res:
				tipos.append(r.tipo_entrada)
			"""
			if res:
				print(d, res)
			else:
				print(d, 'no vino')
			"""
			dictc['fecha']= d
			dictc['tiqueo'] = res
			dictc['t1'] = set([1,2]).issubset(set(tipos))
			dictc['t2'] = set([3,4]).issubset(set(tipos))
			dictc['fopg'] = permiso1(perg, d)
			dictc['fopp'] = permiso_personal1(permp, d)
			dictc['feriado'] = feriado1(d)
			#import pdb; pdb.set_trace()
			#print(dictc)
			estado_final.append(dictc)

		horas = 0
		fopg = 0
		fopp = 0
		for hh in estado_final:
			#import pdb; pdb.set_trace()
			if(hh['fopg'] or hh['fopp'] or hh['feriado']):
				horas=horas+8
				if(hh['fopg']):
					fopg = fopg +8
				if(hh['fopp']):
					fopp = fopp +8
				continue

			if(hh['t1'] and hh['t2']):
				horas=horas+8
			elif(hh['t1'] or hh['t2']):
				horas=horas+4

		instance['horas'] = horas
		instance['fopg'] = fopg
		instance['fopp'] = fopp
		return instance

class KardexUserPDF(WeasyTemplateResponseMixin, KardexUser):
	pass
