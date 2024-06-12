from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.

CATEGORIES = (
    ('Housing', 'Housing'),
    ('Utilities', 'Utilities'),
    ('Groceries', 'Groceries'),
    ('Transportation', 'Transportation'),
    ('Insurance', 'Insurance'),
    ('Healthcare', 'Healthcare'),
    ('Entertainment', 'Entertainment'),
    ('Food', 'Food'),
    ('Education', 'Education'),
    ('Savings', 'Savings'),
    ('Debt Repayment', 'Debt Repayment'),
    ('Clothing', 'Clothing'),
    ('Personal Care', 'Personal Care'),
    ('Gifts & Donations', 'Gifts & Donations'),
    ('Travel', 'Travel'),
    ('Subscriptions', 'Subscriptions'),
    ('Miscellaneous', 'Miscellaneous'),
)

class Expenditures(models.Model):
    amount = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=200,choices=CATEGORIES)
    date = models.DateField(default=now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.category
    
    class Meta:
        verbose_name_plural = 'Expenditures'
        ordering = ['-date']
