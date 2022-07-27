
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import Pet, Member
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import Member, Pet 


    
class MemberForm(ModelForm):
	class Meta:
		model = Member
		fields = '__all__'


class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']



# SEX_CHOICES = ['MALE', 'FEMALE']
# STATUS_CHOICES = ['LOST', 'FOUND']
# TYPE_CHOICES = ['DOG', 'CAT', 'OTHER']


# class PetForm(ModelForm):
#   class Meta:
#     model = Pet
#     fields = ['name', 'city', 'state', 'type', 'breed', 'sex', 'comments', 'status', 'phone']
#     name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name', 'style': 'width: 300px', 'class': 'text-field'}))
#     city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'City', 'style': 'width: 300px', 'class': 'text-field'}))
#     state = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'State', 'style': 'width: 300px', 'class': 'text-field'}))
#     type = forms.ChoiceField(widget=forms.Select(attrs={'placeholder': 'Pet type', 'style': 'width: 300px', 'class': 'custom-select'}), choices=TYPE_CHOICES)
#     breed = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Pet breed', 'style': 'width: 300px', 'class': 'text-field'}))
#     sex = forms.ChoiceField(widget=forms.Select(attrs={'placeholder': 'Pet gender', 'style': 'width: 300px', 'class': 'custom-select'}), choices=SEX_CHOICES)
#     comments = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Comments', 'style': 'width: 300px', 'class': 'text-field'}))
#     status = forms.ChoiceField(widget=forms.Select(attrs={'placeholder': 'This pet has been', 'style': 'width: 300px', 'class': 'custom-select'}), choices=STATUS_CHOICES)
#     phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone', 'style': 'width: 300px', 'class': 'form-control'}))
#     exclude = ['user']
  


class PetForm(ModelForm):
  class Meta:
    model = Pet
    fields = '__all__'
    exclude = ['user', 'member']
