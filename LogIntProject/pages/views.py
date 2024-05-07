from django.shortcuts import render

def index(request):
    return render(request, 'pages/home.html')

def history(request):
    return render(request, 'pages/history.html')

def reports(request):
    return render(request, 'pages/reports.html')

def sources(request):
    return render(request, 'pages/sources.html')

def home(request):
    return render(request, 'pages/home.html')