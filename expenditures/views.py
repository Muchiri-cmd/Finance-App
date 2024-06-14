from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
#from .models import CATEGORIES
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.urls import reverse
from usersettings.models import Settings
import csv
import xlwt
from datetime import date
import datetime


# Create your views here.
@login_required(login_url='/users/login')
def index(request):
    categories = CATEGORIES
    expeditures = Expenditures.objects.filter(user=request.user)
    
    paginator = Paginator(expeditures,5)
    page_number = request.GET.get('page')

    page_object = Paginator.get_page(paginator,page_number)

    currency = Settings.objects.get(user=request.user).currency

    context = {
        "categories":categories,
        "expenditures":expeditures,
        "page_object":page_object,
        "currency":currency,
    }
    return render(request,'expenditures/index.html',context)

def add_expense(request):
    categories = CATEGORIES
    context = {
        "categories":categories,
    }
    if request.method != 'POST': #Get
        return render(request,'expenditures/add-expense.html',context)
    
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']


        Expenditures.objects.create(amount=amount,description=description,category=category,date=date,user=request.user)
        messages.success(request,'Expenditure recorded successfully')

    return redirect('expenditures:index')
        
def edit_expenditure(request,id):
    expenditure = Expenditures.objects.get(pk=id)
    context = {
        "categories":CATEGORIES,
        "expenditure":expenditure,
    }
    if request.GET:   
        return render(request,'expendituresedit-expenditure.html',context)
    elif request.POST:
        expenditure.amount= request.POST['amount']
        expenditure.description = request.POST['description']
        expenditure.category=request.POST['category']
        expenditure.date = request.POST['date']
        expenditure.user=request.user

        expenditure.save()
        messages.success(request,"Record updated successfully")
        return redirect('expenditures:index')
    
    return render(request,'expenditures/edit-expenditure.html',context)

def delete_expenditure(request,id):
    expenditure = Expenditures.objects.get(pk=id)
    expenditure.delete()
    messages.success(request,"Record deleted successfully")

    return redirect('expenditures:index')

from django.http import JsonResponse, HttpResponse
import json

def search_records(request):
    if request.method == "POST":
        query = json.loads(request.body).get('searchText')
        
        expenditures = Expenditures.objects.filter(
            amount__istartswith=query, user=request.user
        ) | Expenditures.objects.filter(
            date__istartswith=query, user=request.user
        ) | Expenditures.objects.filter(
            description__icontains=query, user=request.user
        ) | Expenditures.objects.filter(
            category__icontains=query, user=request.user
        )
        
        data = [
            {
                'id': expenditure.id,
                'amount': expenditure.amount,
                'category': expenditure.category,
                'description': expenditure.description,
                'date': expenditure.date.strftime('%Y-%m-%d'),
                'edit_url': reverse('expenditures:edit-expenditure', args=[expenditure.id]),
                'delete_url': reverse('expenditures:delete-expenditure', args=[expenditure.id]),
            }
            for expenditure in expenditures
        ]
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse(status=405)  # Method Not Allowed

def expenditures_summary(request):
    todays_date = date.today()
    six_months_ago_date =  six_months_ago_date = todays_date - datetime.timedelta(days=30*6)

    six_months_ago_date_str = six_months_ago_date.strftime('%Y-%m-%d')
    todays_date_str = todays_date.strftime('%Y-%m-%d')

    expenditures = Expenditures.objects.filter(date__gte=six_months_ago_date_str,date__lte=todays_date_str,user=request.user)

    finalreport = {}

    def get_category(expenditure):
        return expenditure.category
    
    category_list = list(set(map(get_category,expenditures)))

    def get_category_expenditure(category):
        amount=0
        filtered_by_category = expenditures.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount

        return amount

    for i in expenditures:
        for j in category_list:
            finalreport[j] = get_category_expenditure(j)

    
    return JsonResponse({'final_report':finalreport},safe=False)

def summary_view(request):
    return render(request,'expenditures/summary.html')

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenditures_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.csv'

    # Create a CSV writer object
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    # Query the expenditures for the current user
    expenditures = Expenditures.objects.filter(user=request.user)

    # Write data rows
    for expenditure in expenditures:
        writer.writerow([expenditure.amount, expenditure.description, expenditure.category, expenditure.date])

    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenditures_' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws= wb.add_sheet('Expenditures')
    row_num=0
    font_style=xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']
    for col in range(len(columns)):
        ws.write(row_num,col,columns[col],font_style)

    rows = Expenditures.objects.filter(user=request.user).values_list('amount', 'description', 'category', 'date')

    for row in rows:
        row_num+=1

        for col in range(len(row)):
            ws.write(row_num,col,str(row[col]),font_style)

    wb.save(response)

    return response