from django.urls import path
from . import views


urlpatterns = [
  path('register/', views.registerPage, name="register"),
  path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
  path('account/', views.accountSettings, name="account"),
  

  path('', views.home, name='home'), #HOME ROUTE
  path('about/', views.about, name='about'), #ABOUT ROUTE
  path('pets/', views.pets_index, name='index'),
  path('pets/<int:pet_id>/', views.pets_detail, name='detail'),
  path('pets/create/', views.PetCreate.as_view(), name='pets_create'),
  path('pets/<int:pet_id>/pet_form_photo/', views.pets_create_photo, name='pets_create_photo'),
  path('pets/<int:pk>/update/', views.PetUpdate.as_view(), name='pets_update'),
  path('pets/<int:pk>/delete/', views.PetDelete.as_view(), name='pets_delete'),
  path('pets/<int:pet_id>/add_photo/', views.add_photo, name='add_photo'),
  path('generate-pdf', views.generate_pdf, name='generate_pdf'),
  path('generate-pdf-through-template', views.generate_pdf_through_template, name='generate_pdf_through_template'),
  path('render-pdf/<int:pet_id>', views.render_pdf, name="render_pdf"),
  path('search_pets', views.search_pets, name='search_pets'),
] 
