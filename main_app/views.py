from django.shortcuts import render

# Create your views here.

S3_BASE_URL='https://s3-us-west-2.amazonaws.com/'
BUCKET='lost-and-hound'

def home(request):
  return render(request, 'home.html')