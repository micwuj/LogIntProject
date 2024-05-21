from django.shortcuts import render
from .models import History
from django.core.paginator import Paginator


def history(request):
    historys = History.objects.all().order_by('-operation_date')
    
    pagination_size = 15
    paginator = Paginator(historys, pagination_size)
    page = request.GET.get('page')
    paged_integrations = paginator.get_page(page)
    
    context = {
        'historys': paged_integrations,
    }
    
    return render(request, 'pages/history.html', context)