from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'expenditures'
urlpatterns = [
    path('',index,name='index'),
    path('add-expense/',add_expense,name='add-expense'),
    path('edit-expenditure/<int:id>/',edit_expenditure,name='edit-expenditure'),
    path('delete-expenditure/<int:id>/',delete_expenditure,name='delete-expenditure'),
    path('search-expenditure/',csrf_exempt(search_records),name='search-expenditure'),
    path('category-expenditure-summary/',expenditures_summary,name='category-expenditure-summary'),
    path('summary',summary_view,name='summary-view'),
    path('export-csv',export_csv,name='export-csv'),
    path('export-xls',export_excel,name='export-xls'),
]
