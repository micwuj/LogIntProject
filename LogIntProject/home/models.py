from datetime import datetime
from django.db import models

class Integration(models.Model):
    integration_name = models.CharField(max_length=200)
    customer = models.CharField(max_length=200)
    driver_id = models.IntegerField()
    source = models.CharField(max_length=500)
    apk_file = models.CharField(max_length=5000)
    sh_script = models.CharField(max_length=5000)
    is_active = models.BooleanField(default=True)
    integration_date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.integration_name