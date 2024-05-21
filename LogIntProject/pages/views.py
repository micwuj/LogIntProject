from django.shortcuts import redirect, render

def reports(request):
    return render(request, 'pages/reports.html')

def sources(request):
    return render(request, 'pages/sources.html')

def emulator(request):
    return render(request, 'pages/emulator.html')

