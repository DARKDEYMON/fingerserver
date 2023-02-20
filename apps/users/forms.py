from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import *

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
