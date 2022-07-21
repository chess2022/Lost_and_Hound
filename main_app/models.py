
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from typing import TYPE_CHECKING
from django.db import models
from django.urls import reverse
# Create your models here.

class Pet(models.Model):
  DOG = 'DG'
  CAT = 'CT'
  OTHER = 'OT'
  PET_TYPE = [
    (DOG, 'Dog'),
    (CAT, 'Cat'),
    (OTHER, 'Other')
  ]
  type = models.CharField(max_length=2, choices=PET_TYPE, default=DOG)
  name = models.CharField(max_length=100, blank=False)
  breed = models.CharField(max_length=100, blank=False)
  city = models.CharField(max_length=100, blank=False)
  state = models.CharField(max_length=100, blank=False)
  breed = models.CharField(max_length=100, blank=False)
  MALE = 'ML'
  FEMALE = 'FM'
  PET_SEX = [
    (MALE, 'Male'),
    (FEMALE, 'Female')
  ]
  sex = models.CharField(max_length=2, choices=PET_SEX, default=MALE)
  comments = models.TextField(blank=True)
  LOST = 'LT'
  FOUND = 'FD'
  STATUS_OPTIONS = [
    (LOST, 'Lost'),
    (FOUND, 'Found')
  ]
  status = models.CharField(max_length=2, choices=STATUS_OPTIONS, default=LOST)
  
  def __str__(self):
    return self.name

  def get_absolute_url(self):
      return reverse("detail", kwargs={'pet_id':self.id})
  

  
