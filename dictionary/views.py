from django.http import HttpResponse
from django.shortcuts import render

from .fillmodel import import_terms_from_data_dir

def fill(request):
	import_terms_from_data_dir()
	return HttpResponse('Done!')

def dict_index(request):
	template_name = 'form.html'
	return render(request, template_name)
# Create your views here.
