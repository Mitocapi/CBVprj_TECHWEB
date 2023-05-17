from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    response= "kinda placeholder <br> kinda not"
    return HttpResponse(response)
