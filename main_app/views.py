import profile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import unauthenticated_user
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Pet, Photo, Member
from .forms import PetForm, CreateUserForm, MemberForm
from io import BytesIO
from django.urls import reverse
from xhtml2pdf import pisa
import uuid
import boto3
from django.db.models import Q
from django.conf import settings
from django.contrib.staticfiles import finders
import os
from django.db.models import Max
from django.http import Http404


S3_BASE_URL='https://s3-us-west-2.amazonaws.com/'
BUCKET='lost-and-hound'



# Create your views here.

# ------------------------- KL-todo apply auth routes ------------------------ #
from django.contrib.auth.decorators import login_required
# Create your views here.


@unauthenticated_user
def registerPage(request):
  error_message = ''
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      user = form.save()
      username = form.cleaned_data.get('username')
      group = Group.objects.get(name='members')
      user.groups.add(group)
      Member.objects.create(
				user=user,
				name=user.username,
        email=user.email,
        profile_pic="profile-image.png"
				)
      messages.success(request, 'Account was created for ' + username)
      return redirect('login')
  else:
    error_message = "Invalid Sign up -try again"  
  form = CreateUserForm()
  context = {'form':form, 'error_message': error_message}
  return render(request, 'accounts/register.html', context)





@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, '/accounts/login.html/', context)


@login_required(login_url='login')
def accountSettings (request):
    member = request.user.member
    form = MemberForm(instance=member)
    pets = Pet.objects.order_by('id')
    if request.method == 'POST':
      form = MemberForm(request.POST, request.FILES, instance=member)
      if form.is_valid():
        form.save()
    context = {'form':form, 'pets':pets}
    return render(request, 'accounts/account_settings.html', context)




def logoutUser(request):
	logout(request)
	return redirect('login')



def home(request):
    pets = Pet.objects.order_by('id')
    return render(request, 'home.html', {'pets':pets })

def about(request):
    return render(request, 'about.html')


def pets_index(request):
  pets = Pet.objects.order_by('name')
  return render(request, 'pets/index.html', {'pets':pets})

def pets_detail(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  pets = Pet.objects.order_by('id')
  pet_form = PetForm()
  return render(request, 'pets/detail.html', {'pet': pet, 'pet_form': pet_form, 'pets': pets})


# @login_required(login_url='login')
def pets_create_photo(request, pet_id):
  pet = Pet.objects.get(id=pet_id)
  pet_form = PetForm()
  return render(request, 'main_app/pet_form_photo.html', {'pet': pet, 'pet_form': pet_form})

class PetList(ListView):
  model = Pet

class PetCreate(LoginRequiredMixin, CreateView):
    form_class = PetForm
    model = Pet
    template_name = 'main_app/pet_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    pk = Pet.objects.aggregate(Max('id')).get('id__max')+1
    success_url = f'/pets/{pk}/pet_form_photo/'




class PetUpdate(LoginRequiredMixin, UpdateView):
  model = Pet
  fields = ['type', 'name', 'city', 'state', 'breed', 'sex', 'comments', 'status', ]
  # success_url = f'/pets/{pk}/pet_form_photo/'



  
  
class PetDelete(LoginRequiredMixin, DeleteView):
  model = Pet
  success_url = '/pets/'
  def get_object(self, queryset=None):
    pet = super(PetDelete, self).get_object()
    if not pet.user == self.request.user:
      raise Http404
    return pet
      



@login_required(login_url='login')
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

def render_pdf(request, pet_id):
    path = "pets/results.html"
    context = {"pet" : Pet.objects.get(id = pet_id)}
    html = render_to_string('pets/results.html',context)
    io_bytes = BytesIO()    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes, link_callback=link_callback) 
    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)

####################################
##  Filter Search for Index page  ##
####################################

def search_pets(request):
  if request.method == "POST":
    searched = request.POST['searched']
    pets = Pet.objects.filter(
      Q(name__icontains=searched) |
      Q(city__icontains=searched) |
      Q(state__icontains=searched)|
      Q(status__icontains=searched)|
      Q(type__icontains=searched)) 
    return render(request, 'search_pets.html', {'searched': searched, 'pets':pets})
  else:
    return render("<h1>Your search returned no matches</h1>")