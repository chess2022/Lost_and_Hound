
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from main_app.forms import signUpForm

# Create your views here.

# ------------------------- KL-todo apply auth routes ------------------------ #
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



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