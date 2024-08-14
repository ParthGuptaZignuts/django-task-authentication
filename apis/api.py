
from django.urls import path
from permissions.views import register_user,login_user,change_password,request_password_reset,reset_password,get_user_detail,update_user,delete_user
from authors.views import all_authors

urlpatterns = [
   #authentication urls 
   path('register-user',register_user),
   path('login-user',login_user),
   path('change-password',change_password),
   path('request-password-reset', request_password_reset,name='request-password-reset'),
   path('reset-password/<uidb64>/<token>',reset_password,name='reset-password'),

   #users urls
   path('users',get_user_detail, name="get_user_detail"),
   path('user/<int:user_id>',get_user_detail, name="get_user_detail"),
   path('update-user',update_user , name="update_user"),
   path('delete-user',delete_user , name="delete_user"),

   #authors urls 
   path('authors/all_authors',all_authors,name="all_authors")
   
]