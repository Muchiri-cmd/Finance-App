from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/users/login')
def index(request):
    return render(request,'expenditures/index.html')

def add_expense(request):
    return render(request,'expenditures/add-expense.html')