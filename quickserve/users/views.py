from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def users(request):
    return HttpResponse ('Here are the list of Unemployed People in your Area')

def profile(request):
    return render(request,'profile.html')

def register(request):
    return render(request,'register.html')