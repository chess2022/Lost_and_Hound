from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('pets/', views.pets_index, name='index'),
  path('pets/<int:pet_id>/', views.pets_detail, name='detail'),
]