from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'), #HOME ROUTE
  path('about/', views.about, name='about'), #ABOUT ROUTE
  path('accounts/signup/', views.signup, name='signup'), #SIGNUP ROUTE 
  path('pets/', views.pets_index, name='index'),
  path('pets/<int:pet_id>/', views.pets_detail, name='detail'),
  path('pets/create/', views.PetCreate.as_view(), name='pets_create'),
  path('pets/<int:pk>/update/', views.PetUpdate.as_view(), name='pets_update'),
  path('pets/<int:pk>/delete/', views.PetDelete.as_view(), name='pets_delete'),
  path('pets/<int:pet_id>/add_photo/', views.add_photo, name='add_photo'),
]
