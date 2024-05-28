from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from home.models import Integration, Integration_Account
from .choices import type_choices
from cryptography.fernet import Fernet
from django.conf import settings
from django.utils import timezone
from sources.models import Source
import requests
import json
from history.models import History
from django.views.decorators.csrf import csrf_exempt


def encrypt_password(password):
    f = Fernet(settings.ENCRYPTION_KEY)
    encoded_pass = password.encode('utf-8')
    encrypted_pass = f.encrypt(encoded_pass)
    
    return encrypted_pass

def decrypt_password(password):
    f = Fernet(settings.ENCRYPTION_KEY)
    decrypted_pass = f.decrypt(password)
    decoded_pass = decrypted_pass.decode('utf-8')
    
    return decoded_pass

def home(request):
    integrations = Integration.objects.all().order_by('-integration_date').filter(is_active=True)
    
    pagination_size = 4
    paginator = Paginator(integrations, pagination_size)
    page = request.GET.get('page')
    paged_integrations = paginator.get_page(page)
    source_choices = {source.source_name: source.source_name for source in Source.objects.all()}
    
    context = {
        'integrations': paged_integrations,
        'source_choices': source_choices,
        'type_choices': type_choices,
    }

    print(pull_data_from_active_sources())
        
    return render(request, 'pages/home.html', context)


def add_integration(request):
    if request.method == 'POST':
        integration_name = request.POST['integration_name']
        app_name = request.POST['app_name']
        source_name = request.POST.get('source')
        type = request.POST['type']
        customer = request.POST['customer']
        apk_file = request.POST['apk_file']
        sh_script = request.POST['sh_script'] 

    source = Source.objects.get(source_name=source_name)
        
    integration = Integration(
            integration_name=integration_name,
            app_name=app_name,
            customer=customer,
            source=source,
            type=type,
            apk_file=apk_file,
            sh_script=sh_script,
            integration_date=timezone.now()
        )
    integration.save()

    return redirect('/home')

def integration_details(request, integration_id):
    integration = get_object_or_404(Integration, pk=integration_id)
    drivers = Integration_Account.objects.filter(integration=integration)
    source_choices = {source.source_name: source.source_name for source in Source.objects.all()}
    
    context = {
        'integration': integration,
        'drivers': drivers,
        'type_choices': type_choices,
        'source_choices': source_choices,
    }

    History(type='Integration', name=integration.integration_name, operation='Added', operation_date=timezone.now()).save()
    
    return render(request, 'pages/integration_details.html', context)
 
def edit_integration(request, integration_id):
    
    if request.method == 'POST':
        integration_id = request.POST['integration_id']
        integration = get_object_or_404(Integration, pk=integration_id)
        
        integration.integration_name = request.POST['integration_name']
        integration.app_name = request.POST['app_name']
        source_name = request.POST['source']
        integration.source = Source.objects.get(source_name=source_name)
        integration.type = request.POST['type']
        integration.customer = request.POST['customer']
        integration.apk_file = request.POST['apk_file']
        integration.sh_script = request.POST['sh_script']
        
        integration.save()
        History(type='Integration', name=integration.integration_name, operation='Edited', operation_date=timezone.now()).save()

    return redirect(f'/home/integration{integration_id}')

def delete_integration(request, integration_id):
    integration = get_object_or_404(Integration, pk=integration_id)
        
    integration.delete()
    History(type='Integration', name=integration.integration_name, operation='Deleted', operation_date=timezone.now()).save()
    
    return redirect(f'/home')

@csrf_exempt
def home_delete_integration(request):
    if request.method == 'POST':
        integrations_pks = request.POST.getlist('integration_pks')
        for integration_pk in integrations_pks:
            Integration.objects.filter(pk=integration_pk).delete()
            
        return redirect(f'/home')

def add_driver_account(request, integration_id):
    integration = get_object_or_404(Integration, pk=integration_id)

    if request.method == 'POST':
        driver_id = request.POST['driver_id']
        login = request.POST['driver_login']
        password = request.POST['driver_password']
            
        Integration_Account(driver_id=driver_id, login=login, password=password, integration=integration).save()
        History(type='Driver', name=login, operation='Added', operation_date=timezone.now()).save()
        
    return redirect(f'/home/integration{integration_id}')

def edit_driver_account(request, integration_id):
    integration = get_object_or_404(Integration, pk=integration_id)

    if request.method == 'POST':
        primary_id = request.POST['primary_id'] 
        driver_id = request.POST['driver_id']
        login = request.POST['driver_login']
        password = request.POST['driver_password']
    
        Integration_Account(pk=primary_id, driver_id=driver_id, login=login, password=password, integration=integration).save()
        History(type='Driver', name=login, operation='Edited', operation_date=timezone.now()).save()
    
    return redirect(f'/home/integration{integration_id}')

def delete_driver_account(request, integration_id):
    if request.method == 'POST':
        driver_id = request.POST.get('driver_id')
        login = request.POST.get('driver_login')
        integration_id = request.POST.get('integration_id')
        integration = get_object_or_404(Integration, pk=integration_id) 
        driver = get_object_or_404(Integration_Account, driver_id=driver_id, integration=integration)
        
        driver.delete()
        History(type='Driver', name=login, operation='Deleted', operation_date=timezone.now()).save()
         
    return redirect(f'/home/integration{integration_id}')

def pull_data_from_active_sources():
    unique_sources = {integration.source for integration in Integration.objects.all()}
    all_data = []
    for source in unique_sources:
        url = source.link
        headers = {
            'X-Metabase-Session': '7ff69bc5-0d55-4216-b643-6cb992a249d0',
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()  # Gets the JSON response
            all_data.append(data)  # Append the data to the list
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    # Save the collected data into a JSON file
    with open('Executoner/data/new_data.json', 'w') as file:
        json.dump(all_data, file, indent=4)

    print("Data has been successfully saved to new_data.json.")
