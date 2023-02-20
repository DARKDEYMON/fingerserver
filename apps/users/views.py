from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView
from django.urls import reverse_lazy
from django.db.models import CharField
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
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
