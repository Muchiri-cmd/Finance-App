from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from .models import *
from usersettings.models import Settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
import json
import xlwt
from datetime import date
import datetime
import csv
# Create your views here.

@login_required(login_url='/users/login')
def index(request):
    sources = SOURCES
    income =Income.objects.filter(user=request.user)
    
    paginator = Paginator(income,5)
    page_number = request.GET.get('page')

    page_object = Paginator.get_page(paginator,page_number)

    currency = Settings.objects.get(user=request.user).currency

    context = {
        "sources":sources,
        "income":income,
        "page_object":page_object,
        "currency":currency,
    }
    return render(request,'income/income.html',context)

@login_required(login_url='/users/login')
def add_income(request):
    sources = SOURCES
    context = {
        "sources":sources,
    }
    if request.method != 'POST': #Get
       return render(request,'income/add-income.html',context)  
    
    if request.method == 'POST':
       amount = request.POST['amount']
       description = request.POST['description']
       source = request.POST['source']
       date = request.POST['date']


       Income.objects.create(amount=amount,description=description,source=source,date=date,user=request.user)
       messages.success(request,'Income recorded successfully')

    return redirect('income:index')
    
def edit_income(request,id):
    income = Income.objects.get(pk=id)
    sources = SOURCES

    context = {
        "sources":sources,
        "income":income,
    }
    if request.GET:   
        return render(request,'income/edit-income.html',context)
    elif request.POST:
        income.amount= request.POST['amount']
        income.description = request.POST['description']
        income.source=request.POST['source']
        income.date = request.POST['date']
        income.user=request.user

        income.save()
        messages.success(request,"Record updated successfully")
        return redirect('income:index')

    return render(request,'income/edit-income.html',context)

def delete_income(request,id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request,"Record deleted successfully")

    return redirect('income:index')

def search_income(request):
    if request.method == "POST":
        query = json.loads(request.body).get('searchText')
        
        incomes = Income.objects.filter(
            amount__istartswith=query, user=request.user
        ) | Income.objects.filter(
            date__istartswith=query, user=request.user
        ) | Income.objects.filter(
            description__icontains=query, user=request.user
        ) | Income.objects.filter(
            source__icontains=query, user=request.user
        )
        
        data = [
            {
                'id': income.id,
                'amount': income.amount,
                'source': income.source,
                'description': income.description,
                'date': income.date.strftime('%Y-%m-%d'),
                'edit_url': reverse('income:edit-income', args=[income.id]),
                'delete_url': reverse('income:delete-income', args=[income.id]),
            }
            for income in incomes
        ]
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse(status=405)  # Method Not Allowed

def income_summary(request):
    todays_date = date.today()
    six_months_ago_date =  six_months_ago_date = todays_date - datetime.timedelta(days=30*6)

    six_months_ago_date_str = six_months_ago_date.strftime('%Y-%m-%d')
    todays_date_str = todays_date.strftime('%Y-%m-%d')

    income = Income.objects.filter(date__gte=six_months_ago_date_str,date__lte=todays_date_str,user=request.user)

    finalreport = {}

    def get_source(income):
        return income.source
    
    source_list = list(set(map(get_source,income)))

    def get_income_source(source):
        amount=0
        filtered_by_source = Income.objects.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount

        return amount

    for i in income:
        for j in source_list:
            finalreport[j] = get_income_source(j)

    
    return JsonResponse({'final_report':finalreport},safe=False)

def summary_view(request):
    return render(request,'income/income-summary.html')

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=income_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.csv'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Amount', 'Description', 'Source', 'Date'])

    # Query the income for the current user
    income = Income.objects.filter(user=request.user)

    # Write data rows
    for i in income:
        writer.writerow([i.amount, i.description, i.source, i.date])

    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=income_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws= wb.add_sheet('income')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Source', 'Date']
    for col in range(len(columns)):
        ws.write(row_num,col,columns[col],font_style)

    rows = Income.objects.filter(user=request.user).values_list('amount', 'description', 'source', 'date')

    for row in rows:
        row_num+=1

        for col in range(len(row)):
            ws.write(row_num,col,str(row[col]),font_style)

    wb.save(response)

    return response