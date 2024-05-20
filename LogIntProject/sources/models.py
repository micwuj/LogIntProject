from django.db import models

class Source(models.Model):
    source_name = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.source_name
