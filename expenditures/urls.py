from django.urls import path
from .views import *

app_name = 'expenditures'

urlpatterns = [
    path('',index,name='index'),
    path('add-expense/',add_expense,name='add-expense'),
]
