from django.shortcuts import render
import os,json
from django.conf import settings
from .models import Settings
from django.contrib import messages

# Create your views here.
def preferences(request):
    user_preferences = None #Settings.objects.get(user=request.user)

    exists= Settings.objects.filter(user=request.user).exists()
    
    if exists:
         user_preferences = Settings.objects.get(user=request.user)

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR,'main/currencies.json')    
    with open(file_path,'r') as json_file:
        data = json.load(json_file)

        for k,v in data.items():
            currency_data.append({'name':k,'value':v})

    #print(currency_data)

    if request.method!='POST':
        context = {
        "currencies":currency_data,
        "user_preferences":user_preferences,
        }
       
        return render(request,'user-settings/preferences.html',context)
    
    elif request.POST :
        currency = request.POST['currency']

        if exists:
            user_preferences.currency=currency
            user_preferences.save()
        else :
            user_preferences=Settings.objects.create(user=request.user,currency=currency)
        
        messages.success(request,'Changes saved')

    context = {
        "currencies":currency_data,
        "user_preferences":user_preferences,
    }
        
    return render(request,'user-settings/preferences.html',context)
       