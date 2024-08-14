
from django.urls import path
from permissions.views import register_user,login_user,change_password,request_password_reset,reset_password

urlpatterns = [
   path('register-user',register_user),
   path('login-user',login_user),
   path('change-password',change_password),
   path('request-password-reset', request_password_reset,name='request-password-reset'),
   path('reset-password/<uidb64>/<token>',reset_password,name='reset-password'),
]