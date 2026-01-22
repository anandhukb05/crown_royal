from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse

def hello_world_view1(request):
    return HttpResponse("Hello world!")

