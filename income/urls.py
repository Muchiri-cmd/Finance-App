from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'income'
urlpatterns = [
    path('',index,name='index'),
    path('add-income/',add_income,name='add-income'),
    path('edit-income/<int:id>/',edit_income,name='edit-income'),
    path('delete-income/<int:id>/',delete_income,name='delete-income'),
    path('search-income/',csrf_exempt(search_income),name='search-income'),
    path('category-expenditure-summary/',income_summary,name='category-expenditure-summary'),
    path('summary',summary_view,name='summary-view'),
    path('export-csv',export_csv,name='export-csv'),
    path('export-xls',export_excel,name='export-xls'),
]

