from django.shortcuts import redirect, render

def history(request):
    return render(request, 'pages/history.html')

def reports(request):
    return render(request, 'pages/reports.html')

def sources(request):
    return render(request, 'pages/sources.html')

def emulator(request):
    return render(request, 'pages/emulator.html')

