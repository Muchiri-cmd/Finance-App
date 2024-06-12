from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
#from .models import CATEGORIES
from .models import *
from django.contrib import messages

# Create your views here.
@login_required(login_url='/users/login')
def index(request):
    categories = CATEGORIES
    expeditures = Expenditures.objects.filter(user=request.user)

    context = {
        "categories":categories,
        "expenditures":expeditures,
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