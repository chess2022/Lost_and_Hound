from typing import TYPE_CHECKING
from django.db import models
from django.urls import reverse
# Create your models here.

class Pet(models.Model):
  class Meta:
    verbose_name_plural = 'pets'
    verbose_name = 'pet'
  DOG = 'DG'
  CAT = 'CT'
  OTHER = 'OT'
  TYPE = [
    (DOG, 'Dog'),
    (CAT, 'Cat'),
    (OTHER, 'Other')
  ]
  name = models.CharField(max_length=100, blank=False)
  breed = models.CharField(max_length=100, blank=False)
  city = models.CharField(max_length=100, blank=False)
  state = models.CharField(max_length=100, blank=False)
  breed = models.CharField(max_length=100, blank=False)
  MALE = 'ML'
  FEMALE = 'FM'
  SEX = [
    (MALE, 'Male'),
    (FEMALE, 'Female')
  ]
  comments = models.TextField(blank=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse("detail", kwargs={'pet_id':self.id})
  

  
  