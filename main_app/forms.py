
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import Pet 

class CreateUserForm(UserCreationForm):
  phone_regex = RegexValidator(regex=r'^([0-9]{3}[\-]{1}[0-9]{3}[\-]{1}[0-9]{4})$')
  phone = forms.CharField(validators=[phone_regex], max_length=17, help_text='Phone number must be entered in the format: 000-000-0000.')
  name = forms.CharField(max_length=30, required=True, help_text='Required.')
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']



# class signUpForm(UserCreationForm):
#   phone_regex = RegexValidator(regex=r'^([0-9]{3}[\-]{1}[0-9]{3}[\-]{1}[0-9]{4})$')
#   phone = forms.CharField(validators=[phone_regex], max_length=17, help_text='Phone number must be entered in the format: 000-000-0000.')
#   first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
#   last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
#   email = forms.EmailField(max_length=254, help_text='Required. Please input a valid email address.')

#   class Meta:
#     model = User
#     fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')


class PetForm(ModelForm):
  class Meta:
    model = Pet
    fields = '__all__'
