from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'users'
urlpatterns = [
    path('signup',SignUpView.as_view(),name='signup'),
    path('validate-username',csrf_exempt(UsernameValidation.as_view()),name='validate-username'),
    path('validate-email',csrf_exempt(EmailValidation.as_view()),name='validate-email'),
    path('activate/<uidb64>/<token>',AccountActivation.as_view(),name='activate-account'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('forgot-password',ForgotPassword.as_view(),name='forgot-password'),
    path('reset-password/<uidb64>/<token>',PasswordReset.as_view(),name='reset-password')
]
