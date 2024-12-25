from django.shortcuts import render
from .models import *

def index(request):
    articles = []
    return render(request, 'articles/index.html', context={}
        )
# Create your views here.
def home(request):
    return render(request=render)