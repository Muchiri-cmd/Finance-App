from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

SOURCES = (
    ('employment', 'Employment Income'),  
    ('business', 'Business Income'),      
    ('investment', 'Investment Income'),  
    ('rental', 'Rental Income'),          
    ('government', 'Government Payments'), 
    ('miscellaneous', 'Miscellaneous')   
)

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    source = models.CharField(max_length=200,choices=SOURCES)
    date = models.DateField(default=now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.source
    
    class Meta:
        verbose_name_plural = 'Income'
        ordering = ['-date']
