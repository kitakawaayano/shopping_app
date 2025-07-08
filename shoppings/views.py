from django.shortcuts import render
from django.views import generic
from .models import Shops

# Create your views here.
class shopping(generic.ListView):
    model = Shops
    template_name = 'shopping/index.html'
    
