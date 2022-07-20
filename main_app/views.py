from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .process import create_pdf 
from django.template.loader import render_to_string
from main_app import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pet 
from .forms import PetForm

# Create your views here.

S3_BASE_URL='https://s3-us-west-2.amazonaws.com/'
BUCKET='lost-and-hound'

def home(request):
  return render(request, 'home.html')

def pets_index(request):
  pets = Pet.objects.filter(user=request.user)
  return render(request, 'pets/index.html', {'pets':pets})

def pets_detail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  pet_form = PetForm()
  return render(request, 'pets/detail.html',{
    'pet': pet, 'pet_form': pet_form
  })

def pets_create(request):
  pass

def pets_delete(request):
  pass

def pets_update(request):
  pass

def home(request):
    return HttpResponse('<h1>Hello World</h1>')

class GeneratePdf(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
        data = models.Pet.objects.all().order_by('first_name')
        open('templates/temp.html', "w").write(render_to_string('result.html', {'data': data}))

        # Converting the HTML template into a PDF file
        pdf = create_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')






