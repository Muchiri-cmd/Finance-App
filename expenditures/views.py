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
