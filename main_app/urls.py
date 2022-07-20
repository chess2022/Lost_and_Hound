from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('pets/', views.pets_index, name='index'),
  path('pets/<int:pet_id>/', views.pets_detail, name='detail'),
  path('pets/create/', views.PetCreate.as_view(), name='pets_create'),
  path('pets/<int:pk>/update/', views.PetsUpdate.as_view(), name='pets_update'),
  path('pets/<int:pk>/delete/', views.PetDelete.as_views(), name='pets_delete'),
]