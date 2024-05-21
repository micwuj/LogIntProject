from django.shortcuts import render
from django.http import JsonResponse
from sources.models import Source
from django.views.decorators.csrf import csrf_exempt


def sources(request):
    sources = Source.objects.all()
    return render(request, 'pages/sources.html', {'sources': sources})

def add_source(request):
    if request.method == 'POST':
        source_name = request.POST.get('source_name')
        link = request.POST.get('link')
        if Source.objects.filter(source_name=source_name).exists():
            return JsonResponse({'error': 'Source with this name already exists'}, status=400)
        new_source = Source.objects.create(source_name=source_name, link=link)
        print(new_source)
        return JsonResponse({'source_name': new_source.source_name, 'link': new_source.link})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def edit_source(request):
    if request.method == 'POST':
        previous_source_name = request.POST.get('previous_source_name')
        source_name = request.POST.get('source_name')
        link = request.POST.get('link')
        if Source.objects.filter(source_name=source_name).exclude(source_name=previous_source_name).exists():
            return JsonResponse({'error': 'Source with this name already exists'}, status=400)
        try:
            source = Source.objects.get(source_name=source_name)
            source.link = link
            source.save()
            return JsonResponse({'success': 'Updated'})
        except Source.DoesNotExist:
            return JsonResponse({'error': 'Source not found'}, status=404)


@csrf_exempt
def delete_source(request):
    if request.method == 'POST':
        source_names = request.POST.getlist('source_names')
        Source.objects.filter(source_name__in=source_names).delete()
        return JsonResponse({'success': 'Deleted'})
