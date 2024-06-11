from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
import json
from validate_email import validate_email
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth

# Create your views here.
class SignUpView(View):
    def get(self,request):
        return render(request,'users/signup.html')
    def post(self,request):
        '''
        messages.success(request,"Success")
        messages.warning(request,"warning")
        messages.info(request,"Info")
        messages.error(request,"error")
        '''
        #Get user data
        username = request.POST['username']
        user_email = request.POST['email']
        password = request.POST['password']

        context = {
            'userinfo': request.POST
        }
        
        #validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=user_email).exists():
               if len(password)<8:
                   messages.error(request,"Password should be at least 8 characters")
                   return render(request,'users/signup.html',context)
         #create user account
        user = User.objects.create_user(username=username,email=user_email)
        user.set_password(password)
        user.is_active=False
        user.save()
    
        #encrypt user id
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('users:activate-account',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
    
        activate_url = f'http://{domain}{link}'

        #seetup email n send  
        email_subject='Activate your account'
        email_body= f"Hi {user.username} Please use this link to activate your account\n {activate_url}"
        

        email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@semycolon.com",
                    [user_email],
                    #["bcc@example.com"],
                    #reply_to=["another@example.com"],
                    headers={"Message-ID": "foo"},
                )
        
        email.send(fail_silently=False)
        messages.success(request,'Account successfully created')

     
        return render(request,'users/signup.html')

class AccountActivation(View):
      #def path to view that will activate user acc
         # 1) get domain we are on  
         # 2) conact relative url to verfifcation view
         # 3) encode uid -way to identify user back n forth thru email verification process
         # 4) token user uses to verify. Shoul be used once
        #email
    def get(self,request,uidb64,token):

        try :
            id = urlsafe_base64_decode(str(uidb64))
            print(id)
            user = User.objects.get(pk=id)
            print(user)

            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User already active')

            if user.is_active:
                return redirect('users:login')
            user.is_active=True
            user.save()

            messages.success(request,'Account activated successfully')
        except Exception as e:
            pass
     
        return redirect('users:login')
    
class LoginView(View):
    def get(self,request):
        return render(request,'users/login.html')
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
       
        if username and password:
            user = auth.authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,f'Welcome, {user.username} . log in successful')
                    return redirect('expenditures:index')

                messages.error(request,'Account is not active.Please check you email to activate account')
                return render(request,'users/login.html')
            
            messages.error(request,'Invalid login credentials.Please try again')
            return render(request,'users/login.html')
        
        messages.error(request,'Please fill in all fields')
        return render(request,'users/login.html')

class LogoutView(View):
     def get(self,request):
         auth.logout(request)
         messages.success(request,'Successfully logged out')
         return redirect('users:login')


class UsernameValidation(View):
    def post(self,request):
        data = json.loads(request.body) #loads json data to an accessible python dictionary
        username = data['username']

        if not str(username).isalnum(): #check if username is alphanumeric
            return JsonResponse({'error':'username should only contain alphanumeric characters'},status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error':'Username already registered , use another one or login if it was you'}, status=409)
        return JsonResponse({'username_valid':True})
        
class EmailValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'error':'email is not valid'}, status = 400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error':'email is already registered.'})
        return JsonResponse({'email_valid':True})
    
