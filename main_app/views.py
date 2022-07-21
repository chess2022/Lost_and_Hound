from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from main_app.forms import signUpForm
from django.contrib.auth import login, authenticate
from .process import create_pdf 
from django.template.loader import render_to_string
from main_app import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pet, Photo
from .forms import PetForm
from django.http import HttpResponse
from django.views.generic import View
from .process import create_pdf 
from django.template.loader import render_to_string
from main_app import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import inlineformset_factory
import uuid
import boto3


S3_BASE_URL='https://s3-us-west-2.amazonaws.com/'
BUCKET='lostandhound'

PhotoFormset = inlineformset_factory(
  Pet, Photo, fields=('url',)
)
# Create your views here.

# ------------------------- KL-todo apply auth routes ------------------------ #
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

# def lostandhound_index(request):
#   return render(request, 'pet/index.html')

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
            return redirect('accounts/login')
        else:
            error_message = 'Invalid sign-up. Please try again'
    form = signUpForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


def pets_index(request):
  pets = Pet.objects.filter(user=request.user)
  return render(request, 'pets/index.html', {'pets':pets})

# def pets_detail(request, pet_id):
#   pet = Pet.objects.get(id=pet_id)
#   pet_form = PetForm()
#   return render(request, 'pets/detail.html',{
#     'pet': pet, 'pet_form': pet_form
#   })

def pets_detail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  pet_form = PetForm()
  return render(request, 'pets/detail.html', {'pet': pet, 'pet_form': pet_form})

class PetList(LoginRequiredMixin, ListView):
  model = Pet

class PetCreate(LoginRequiredMixin, CreateView):
  model = Pet
  fields = '__all__'

  def get_context_data(self, **kwargs):
    # need to overwrite to get_context_data to make sure formset is rendered
    data = super().get_context_data(**kwargs)
    if self.request.POST:
      data["photos"] = PhotoFormset(self.request.POST, self.request.FILES.get('data', None), instance=self.object)
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + data[data.rfind('.'):]
      print(key)
    try:
        s3.upload_fileobj(data, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        photo = Photo(url=url)
        photo.save()
    except:
      print(("Photo upload to S3 unsuccessful"))
    else:
      data["photos"] = PhotoFormset()
    return data

  def form_valid(self, form):
    context = self.get_context_data()
    photos = context["photos"]
    self.object = form.save()
    if photos.is_valid():
      photos.instance = self.object
      photos.save()
    return super().form_valid(form)
  def get_success_url(self):
    return reverse("pets:list")

  def form_valid(self, form):
    context = self.get_context_data()
    photo = context["photo"]
    self.object = form.save()
    if photo.is_valid():
      photo.instance = self.object
      photo.save()
    # form.instance.user = self.request.user
    return super().form_valid(form)

class PetUpdate(UpdateView):
  model = Pet
  fields = '__all__'

class PetDelete(DeleteView):
  model = Pet
  success_url = '/pets/'
  

class GeneratePdf(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
        data = models.Pet.objects.all().order_by('first_name')
        open('templates/temp.html', "w").write(render_to_string('result.html', {'data': data}))

        # Converting the HTML template into a PDF file
        pdf = create_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

# def add_photo(request, pet_id):
#   photo_file = request.FILES.get('photo-file', None)
#   if photo_file:
#     s3 = boto3.client('s3')
#     key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
#     print(key)
#     try:
#         s3.upload_fileobj(photo_file, BUCKET, key)
#         url = f"{S3_BASE_URL}{BUCKET}/{key}"
#         photo = Photo(url=url)
#         photo.save()
#     except:
#       print(("Photo upload to S3 unsuccessful"))
#   return redirect('pets/create', pet_id='pet_id')

