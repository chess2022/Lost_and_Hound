from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import unauthenticated_user
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Member, Pet, Photo
from .forms import PetForm, CreateUserForm
from io import BytesIO
from xhtml2pdf import pisa
import uuid
import boto3

S3_BASE_URL='https://s3-us-west-2.amazonaws.com/'
BUCKET='lost-and-hound'



# Create your views here.

# ------------------------- KL-todo apply auth routes ------------------------ #
from django.contrib.auth.decorators import login_required
# Create your views here.

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='member')
			user.groups.add(group)
			Member.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
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
	return render(request, '/accounts/login/', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


def userPage(request):
	profile = request.user.member._set.all()

	return render(request, 'accounts/user.html')


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


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

class PetList(ListView):
  model = Pet

class PetCreate(LoginRequiredMixin, CreateView):
    model = Pet
    fields = '__all__'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    pk = Pet.objects.latest('id').id+1
    success_url = f'/pets/{pk}/pet_form_photo/'

class PetUpdate(LoginRequiredMixin, UpdateView):
  model = Pet
  fields = '__all__'

class PetDelete(DeleteView):
  model = Pet
  success_url = '/pets/'


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
    context = {"pet" : Pet.objects.get(id=pet_id), "user": request.user.id}
    html = render_to_string('pets/results.html',context)
    io_bytes = BytesIO()    
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)   
    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)