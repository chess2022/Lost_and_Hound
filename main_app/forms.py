
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class signUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  email = forms.EmailField(max_length=254, help_text='Required. Please input a valid email address.')

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
from django.forms import ModelForm
from .models import Pet 

class PetForm(ModelForm):
  class Meta:
    model = Pet
    fields = '__all__'
