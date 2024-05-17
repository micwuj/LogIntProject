from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from home.models import Integration
from .choices import source_choices, type_choices

def home(request):
    integrations = Integration.objects.all().order_by('-integration_date').filter(is_active=True)
    
    pagination_size = 4
    paginator = Paginator(integrations, pagination_size)
    page = request.GET.get('page')
    paged_integrations = paginator.get_page(page)
    
    context = {
        'integrations': paged_integrations,
        'source_choices': source_choices,
        'type_choices': type_choices,
    }
        
    return render(request, 'pages/home.html', context)

def integration(request):
    if request.method == 'POST':
        integration_name = request.POST['integration_name']
        driver_login = request.POST['driver_login']
        driver_password = request.POST['driver_password']
        source = request.POST['source']
        type = request.POST['type']
        customer = request.POST['customer']
        apk_file = request.POST['apk_file']
        sh_script = request.POST['sh_script'] 

        # Check if integration exists already
        # already_exist = Integration.objects.all().filter(integration_id=integration_id, user_id=user_id)
        # if has_contacted:
        #     messages.error(request, "Request already has been sent for this listing")
        #     return redirect('/listings/'+listing_id)

        integration = Integration(integration_name=integration_name, customer=customer, source=source,  type=type, apk_file=apk_file, sh_script=sh_script)
        integration.save()


        # messages.success(request, 'Your request has been sent!')

    return redirect('/home')
