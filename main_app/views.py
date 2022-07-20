from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .process import create_pdf 
from django.template.loader import render_to_string
from main_app import models
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

def home(request):
    return HttpResponse('<h1>Hello World</h1>')

class GeneratePdf(LoginRequiredMixin, View):
     def get(self, request, *args, **kwargs):
        data = models.Pet.objects.all().order_by('first_name')
        open('templates/temp.html', "w").write(render_to_string('result.html', {'data': data}))

        # Converting the HTML template into a PDF file
        pdf = create_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

