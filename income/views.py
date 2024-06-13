from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from .models import *
from usersettings.models import Settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
import json
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
     