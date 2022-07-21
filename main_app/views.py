
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from main_app.forms import signUpForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pet 
from .forms import PetForm
from django.http import HttpResponse
from django.views.generic import View
from .process import create_pdf 
from django.template.loader import render_to_string
from main_app import models
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

# ------------------------- KL-todo apply auth routes ------------------------ #
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def lostandhound_index(request):
  return render(request, 'pet/index.html')

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign-up. Please try again'
    form = signUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# Create your views here.

S3_BASE_URL='https://s3-us-west-2.amazonaws.com/'
BUCKET='lost-and-hound'


def pets_index(request):
  pets = Pet.objects.filter(user=request.user)
  return render(request, 'pets/index.html', {'pets':pets})

def pets_detail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  pet_form = PetForm()
  return render(request, 'pets/detail.html',{
    'pet': pet, 'pet_form': pet_form
  })


# Create your views here.

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

