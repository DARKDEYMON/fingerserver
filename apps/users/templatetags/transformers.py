from django import template
import holidays
from apps.users.models import *

register = template.Library()

@register.filter(name='tickeos_vacios')
def tickeos_vacios(array):
	res = []
	for p in range(1,5):
		addet = False
		for c in array:
			if c.tipo_entrada == p:
				res.append(c)
				addet = True
				break
		if not addet:
			res.append(None)
	return res

@register.filter(name='tickeos_vacioshc')
def tickeos_vacioshc(array):
	res = []
	for p in range(1,3):
		addet = False
		for c in array:
			if c.tipo_entrada == p:
				res.append(c)
				addet = True
				break
		if not addet:
			res.append(None)
	return res

@register.simple_tag
def feriado(date):
	potosi = holidays.country_holidays('BO', subdiv='P')
	if date in potosi:
		return potosi.get(date)
	else:
		return None

@register.simple_tag
def fin_semana(date):
	if(date.weekday() == 5 or date.weekday() == 6):
		return True
	else:
		return None

@register.simple_tag
def permiso(date):
	res = PermisosGenerales.objects.all()
	#import pdb; pdb.set_trace()
	for r in res:
		if(r.fecha_inicio == r.fecha_fin and date['fecha']==r.fecha_inicio):
			return r
		elif(r.fecha_inicio<=date['fecha']<=r.fecha_fin):
			return r
		return None

@register.simple_tag
def permiso_personal(user, date):
	res = Permisos.objects.filter(user=user)
	#import pdb; pdb.set_trace()
	for r in res:
		if(r.fecha_inicio == r.fecha_fin and date['fecha']==r.fecha_inicio):
			return r
		elif(r.fecha_inicio<date['fecha']<r.fecha_fin):
			return r
		return None

def permiso1(res, date):
	res = PermisosGenerales.objects.all()
	#import pdb; pdb.set_trace()
	for r in res:
		if(r.fecha_inicio == r.fecha_fin and date==r.fecha_inicio):
			return r
		elif(r.fecha_inicio<=date<=r.fecha_fin):
			return r
		return None

def permiso_personal1(res, date):
	for r in res:
		#import pdb; pdb.set_trace()
		if(r.fecha_inicio == r.fecha_fin and date==r.fecha_inicio):
			return r
		elif(r.fecha_inicio<=date<=r.fecha_fin):
			return r
		return None

def feriado1(date):
	potosi = holidays.country_holidays('BO', subdiv='P')
	if date in potosi:
		return potosi.get(date)
	else:
		return None