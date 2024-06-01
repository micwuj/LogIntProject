from django.shortcuts import render
from django.http import JsonResponse
from sources.models import Source
from django.views.decorators.csrf import csrf_exempt

def emulator(request):
    return render(request, 'pages/emulator.html')

