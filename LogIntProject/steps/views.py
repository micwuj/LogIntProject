from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
import os
from .models import Steps
from home.models import Integration
from django.db.models import Max

def add_step(request, integration_id):
    if request.method == 'POST':
        integration_id = request.POST.get('integration_id')
        action = request.POST.get('action')
        img = request.FILES.get('screenshot')
        input_value = request.POST.get('input_value')
        integration = Integration.objects.get(pk=integration_id)
        
        max_step_number = Steps.objects.filter(integration=integration).aggregate(Max('step_number'))['step_number__max']
        
        if max_step_number is None:
            max_step_number = 0
        
        unused_step_number = None
        for i in range(1, max_step_number + 2):
            if not Steps.objects.filter(integration=integration, step_number=i).exists():
                unused_step_number = i
                break
        
        if unused_step_number is None:
            step_number = 1
        else:
            step_number = unused_step_number
        
        step = Steps(
            step_number=step_number,
            action=action,
            img=img,
            input_value=input_value,
            integration=integration
        )
        
        if img:
            img_name = step.change_img_name(img.name)
            step.img.name = img_name
        
        step.save()
        
    return redirect(f'/home/integration{integration_id}')

def delete_step(request, integration_id):
    if request.method == 'POST':
        step_pk = request.POST.get('step_pk')
        step = get_object_or_404(Steps, pk=step_pk)
        integration_id = step.integration.pk
        
        if step.img:
            img_path = os.path.join(settings.MEDIA_ROOT, str(step.img))
            if os.path.exists(img_path):
                os.remove(img_path)
        
        step.delete()
        messages.success(request, "Step deleted successfully.")
    
    return redirect(f'/home/integration{integration_id}')

def edit_step(request, integration_id):
    if request.method == 'POST':
        step_pk = request.POST.get('step_pk')
        action = request.POST.get('step_action')
        img = request.FILES.get('step_img')
        input_value = request.POST.get('step_input_value')

        step = get_object_or_404(Steps, pk=step_pk)

        if step.action != action:
            step.action = action
            if img:
                if step.img:
                    img_path = os.path.join(settings.MEDIA_ROOT, str(step.img))
                    if os.path.exists(img_path):
                        os.remove(img_path)
            else:
                img_path = os.path.join(settings.MEDIA_ROOT, str(step.img))
                if os.path.exists(img_path):
                    new_img_name = step.change_img_name(step.img.name)
                    new_img_path = os.path.join(settings.MEDIA_ROOT, new_img_name)
                    os.rename(img_path, new_img_path)
                    step.img.name = new_img_name

        step.input_value = input_value

        if img:
            if step.img:
                    img_path = os.path.join(settings.MEDIA_ROOT, str(step.img))
                    if os.path.exists(img_path):
                        os.remove(img_path)
            img_name = step.change_img_name(img.name)
            step.img = img
            step.img.name = img_name

        step.save()

    return redirect(f'/home/integration{integration_id}')