from django.shortcuts import render
from django.http import JsonResponse
from sources.models import Source
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'pages/home.html')

def history(request):
    return render(request, 'pages/history.html')

def reports(request):
    return render(request, 'pages/reports.html')

def emulator(request):
    return render(request, 'pages/emulator.html')

