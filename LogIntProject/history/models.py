from django.db import models

class History(models.Model):
    # user = User()
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    operation = models.CharField(max_length=50)
    operation_date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.type} | {self.name} | {self.operation}"