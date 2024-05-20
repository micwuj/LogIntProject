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

def sources(request):
    sources = Source.objects.all()
    return render(request, 'pages/sources.html', {'sources': sources})

def add_source(request):
    if request.method == 'POST':
        source_name = request.POST.get('source_name')
        link = request.POST.get('link')
        new_source = Source.objects.create(source_name=source_name, link=link)
        return JsonResponse({'source_name': new_source.source_name, 'link': new_source.link})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def edit_source(request):
    if request.method == 'POST':
        source_id = request.POST.get('id')
        source_name = request.POST.get('source_name')
        link = request.POST.get('link')
        source = Source.objects.get(id=source_id)
        source.source_name = source_name
        source.link = link
        source.save()
        return JsonResponse({'success': 'Updated'})

@csrf_exempt
def delete_source(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids')
        Source.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': 'Deleted'})


def home(request):
    return render(request, 'pages/home.html')

def emulator(request):
    return render(request, 'pages/emulator.html')