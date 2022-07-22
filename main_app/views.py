import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from main_app.forms import signUpForm
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Pet, Photo
from .forms import PetForm
from io import BytesIO
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.conf import settings
from django.contrib.auth.models import User
import uuid
import boto3


S3_BASE_URL='https://s3-us-west-2.amazonaws.com/'
BUCKET='lostandhound'


# Create your views here.

# ------------------------- KL-todo apply auth routes ------------------------ #
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


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

@login_required
def pets_index(request):
  pets = Pet.objects.order_by('name')
  return render(request, 'pets/index.html', {'pets':pets})

def pets_detail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  pet_form = PetForm()
  return render(request, 'pets/detail.html', {'pet': pet, 'pet_form': pet_form})

def pets_create_photo(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  pet_form = PetForm()
  return render(request, 'main_app/pet_form_photo.html', {'pet': pet, 'pet_form': pet_form})

class PetList(LoginRequiredMixin, ListView):
  model = Pet

class PetCreate(LoginRequiredMixin, CreateView):
    model = Pet
    fields = '__all__'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    success_url = '/pets/'

class PetUpdate(LoginRequiredMixin, UpdateView):
  model = Pet
  fields = '__all__'

class PetDelete(DeleteView):
  model = Pet
  success_url = '/pets/'

@login_required
def add_photo(request, pet_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f"{S3_BASE_URL}{BUCKET}/{key}"
        photo = Photo(url=url, pet_id=pet_id)
        photo.save()
    except:
      print(("Photo upload unsuccessful"))
  return redirect('detail', pet_id=pet_id)


#####################################
##      pdf generation views       ##
#####################################

def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
            if not isinstance(result, (list, tuple)):
                result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
        else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                path = os.path.join(mRoot, uri.replace(mUrl, ""))
            elif uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
            else:
                return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path



def generate_pdf(request):
    html = '<html><body><p>To PDF or not to PDF</p></body></html>'
    write_to_file = open('media/test.pdf', "w+b")
    result = pisa.CreatePDF(html,dest=write_to_file)
    write_to_file.close()
    return HttpResponse(result.err)

def generate_pdf_through_template(request):
    context={}
    html = render_to_string('pdf/results',context)   
    write_to_file = open('media/test_1.pdf', "w+b")   
    result = pisa.CreatePDF(html,dest=write_to_file)  
    write_to_file.close()   
    return HttpResponse(result.err)

def render_pdf(request):
    path = "pets/results.html"
    # user = request.user
    context = {"pets" : Pet.objects.all()[:100]}
    html = render_to_string('pets/results.html',context)
    io_bytes = BytesIO()    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)   
    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)
