from django.urls import path
from .views import *

app_name = 'expenditures'

urlpatterns = [
    path('',index,name='index'),
    path('add-expense/',add_expense,name='add-expense'),
    path('edit-expenditure/<int:id>/',edit_expenditure,name='edit-expenditure'),
    path('delete-expenditure/<int:id>/',delete_expenditure,name='delete-expenditure')
]
