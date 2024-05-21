from datetime import datetime
from django.db import models
from sources.models import Source

class Integration(models.Model):
    integration_name = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100)
    customer = models.CharField(max_length=100) 
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    apk_file = models.CharField(max_length=5000)
    sh_script = models.CharField(max_length=5000)
    is_active = models.BooleanField(default=True)
    integration_date = models.DateTimeField(blank=True)

    def __str__(self):
        return self.integration_name

class Integration_Account(models.Model):
    driver_id = models.IntegerField(primary_key=True)
    login = models.CharField()
    password = models.CharField()
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.login
