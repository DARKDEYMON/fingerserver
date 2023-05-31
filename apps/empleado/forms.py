from django import forms
from .models import *

class QuejasForm(forms.ModelForm):
	class Meta:
		model = Quejas
		exclude = ['user']

class RequerimientoForm(forms.ModelForm):
	class Meta:
		model = Requerimiento
		exclude = ['user','atendido']
