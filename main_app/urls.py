from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'), #HOME ROUTE
  path('about/', views.about, name='about'), #ABOUT ROUTE
  path('index/', views.lostandhound_index, name='index'), #INDEX ROUTE - show all lost pets
  path('accounts/signup/', views.signup, name='signup'), #SIGNUP ROUTE 
  path('pets/<int:pet_id>/', views.pets_detail, name='detail'),
]