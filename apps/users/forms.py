from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField
from constance import config
from django.conf import settings
from datetime import time
from .models import *

class Html5DateInput(forms.DateInput):
	input_type = 'date'
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.format = ('%Y-%m-%d')

class search_form(forms.Form):
	search = forms.CharField(required=False, label="", help_text="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Buscar...'}))

class CreateUserForm(UserCreationForm):
	class Meta:
		model=User
		fields=[
			'username',
			'first_name',
			'last_name',
			'email',
		]
	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True

class UpdateUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = {
			'first_name',
			'last_name',
			'email'
		}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True

class MetricasForm(forms.ModelForm):
	class Meta:
		model = Metricas
		exclude = ['user']

class MetricasHelperForm(FormHelper):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.form_method = 'post'
		self.layout = Layout(
			Row(
				Column('imagen', css_class="col-lg-6"),
				Column('DELETE', css_class="d-flex align-items-center pt-3"),
				css_class='g-1',
			),
			HTML('<hr class="border border-primary border-3 opacity-75">')

		)
		self.render_required_fields = True
		self.form_tag = False

metricas_inline = inlineformset_factory(User, Metricas, form=MetricasForm, extra=1, can_delete=True)

class ConstanceForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for key in self.Meta.constance_values.keys():
			data = self.Meta.constance_values[key]
			typo = self.getDataOrNone(data,2)
			if not typo or typo==str:
				self.fields[key] = forms.CharField(label=data[1], required=True, initial=getattr(self.Meta.constance,key))
			elif(typo==bool):
				self.fields[key] = forms.BooleanField(label=data[1], required=True, initial=getattr(self.Meta.constance,key))
			elif(typo==int):
				self.fields[key] = forms.IntegerField(label=data[1], required=True, initial=getattr(self.Meta.constance,key))
			elif(typo==float):
				self.fields[key] = forms.FloatField(label=data[1], required=True, initial=getattr(self.Meta.constance,key))
			elif(typo==time):
				self.fields[key] = forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'), label=data[1], required=True, initial=getattr(self.Meta.constance,key))
	def getDataOrNone(self, data, index):
		try:
			return data[index]
		except Exception as e:
			return None
	def save(self):
		for key in self.cleaned_data:
			setattr(self.Meta.constance, key, self.cleaned_data[key])
	class Meta:
		constance = config
		constance_values = settings.CONSTANCE_CONFIG

class DateForm(forms.Form):
	inicio = forms.DateField(widget=Html5DateInput, required = True)
	fin = forms.DateField(widget=Html5DateInput, required = True)
