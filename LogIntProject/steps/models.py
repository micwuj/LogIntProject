import os
from django.db import models
from django.db import models
from home.models import Integration

TYPE_IN = 'TYP'
TAP = 'TAP'
SELECT = 'SEL'

ACTION_CHOICES = {
    TYPE_IN: 'TYPE IN',
    TAP: 'TAP',
    SELECT: 'SELECT'
}

class Steps(models.Model):
    step_number = models.IntegerField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES.items())
    img = models.ImageField()
    input_value = models.CharField(max_length=128, null=True, blank=True)
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Step number: ' + str(self.step_number) + ' - action: ' + self.action
    
    def change_img_name(self, filename):
        _, ext = os.path.splitext(filename)
        new_filename = f"{self.integration.pk}_{self.step_number}_{self.action}{ext}"
        return new_filename