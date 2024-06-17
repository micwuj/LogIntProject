from django.shortcuts import render

def emulator(request):
    return render(request, 'pages/emulator.html')

