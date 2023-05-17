from django import template
import holidays

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
