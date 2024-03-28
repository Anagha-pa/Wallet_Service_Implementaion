from django.db import models

# Create your models here.


class BaseModel(models.Model):
    
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True