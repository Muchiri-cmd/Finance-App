from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Settings(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    currency = models.CharField(max_length=255,blank=True,null=True)
    #other user preferences and custom settings

    def __str__(self):
        return f"{self.user} preferences"
    
