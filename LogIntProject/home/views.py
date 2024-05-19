from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from home.models import Integration, Integration_Account
from .choices import source_choices, type_choices
from cryptography.fernet import Fernet
from django.conf import settings
from datetime import datetime
from django.utils import timezone
import pytz

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
    
    context = {
        'integrations': paged_integrations,
        'source_choices': source_choices,
        'type_choices': type_choices,
    }
        
    return render(request, 'pages/home.html', context)

def integration(request):
    if request.method == 'POST':
        integration_name = request.POST['integration_name']
        app_name = request.POST['app_name']
        source = request.POST['source']
        type = request.POST['type']
        customer = request.POST['customer']
        apk_file = request.POST['apk_file']
        sh_script = request.POST['sh_script'] 
        
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
        
        
    #     # Check if the post request is for editing
    #     integration_id = request.POST.get('integration_id')
    #     if integration_id:
    #         integration = get_object_or_404(Integration, id=integration_id)
    #         integration.integration_name = integration_name
    #         integration.app_name = app_name
    #         integration.source = source
    #         integration.type = type
    #         integration.customer = customer
    #         integration.apk_file = apk_file
    #         integration.sh_script = sh_script
    #         integration.integration_date = timezone.now()
    #         integration.save()
    #     else:
    #         integration = Integration(
    #             integration_name=integration_name,
    #             app_name=app_name,
    #             customer=customer,
    #             source=source,
    #             type=type,
    #             apk_file=apk_file,
    #             sh_script=sh_script,
    #             integration_date=timezone.now()
    #         )
    #         integration.save()

    #     # messages.success(request, 'Your request has been sent!')

    # return redirect('/home')

def integration_account(request):
    if request.method == 'POST':
        driver_id = request.POST['driver_id']
        login = encrypt_password(request.POST['login'])
        password = request.POST['password']
        
    driver_already_exist = Integration_Account.objects.all().filter(driver_id=driver_id)
    if not driver_already_exist:
        driver = Integration_Account(driver_id=driver_id, login=login, password=password)
        driver.save()
    else:
        pass
