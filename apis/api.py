from django.urls import path
from permissions.views import register_user,login_user,logout_user,change_password,request_password_reset,reset_password,get_user_detail,update_user,delete_user
from authors.views import all_authors
from products.views import all_products,single_product,update_product,create_product,delete_product
from Compaines.views import all_companies, single_company, create_company, update_company, delete_company ,all_departments,single_department,create_department,update_department,delete_department,all_employees,single_employee,create_employee,update_employee,delete_employee,all_addresses,single_address,create_address,update_address,delete_address,all_projects,single_project,create_project,update_project,delete_project,all_tasks,single_task,create_task,update_task,delete_task

urlpatterns = [
    
   #authentication urls 
   path('register-user',register_user),
   path('login-user',login_user),
   path('logout-user',logout_user),
   path('change-password',change_password),
   path('request-password-reset', request_password_reset,name='request-password-reset'),
   path('reset-password/<uidb64>/<token>',reset_password,name='reset-password'),

   #users urls
   path('users',get_user_detail, name="get_user_detail"),
   path('user/<int:user_id>',get_user_detail, name="get_user_detail"),
   path('update-user',update_user , name="update_user"),
   path('delete-user',delete_user , name="delete_user"),

   #authors urls 
   path('authors/all_authors',all_authors,name="all_authors"),

   #products urls
   path('products/all-products',all_products, name='all_products'),
   path('products/<int:product_id>/',single_product, name='single_product'),
   path('products/create/',create_product, name='create_product'),
   path('products/update/<int:product_id>/',update_product, name='update_product'),
   path('products/delete/<int:product_id>/',delete_product, name='delete_product'),
   
   path('companies/all-companies',all_companies, name='all_companies'),
   path('companies/<int:company_id>/',single_company, name='single_company'),
   path('companies/create/',create_company, name='create_company'),
   path('companies/<int:company_id>/update/',update_company, name='update_company'),
   path('companies/<int:company_id>/delete/',delete_company, name='delete_company'),
    
    # Department URLs
   path('departments/all-departments', all_departments, name='all_departments'),
   path('departments/<int:department_id>/', single_department, name='single_department'),
   path('departments/create/', create_department, name='create_department'),
   path('departments/<int:department_id>/update/', update_department, name='update_department'),
   path('departments/<int:department_id>/delete/', delete_department, name='delete_department'),
    
    # Employee URLs
   path('employees/all-employees', all_employees, name='all_employees'),
   path('employees/<int:employee_id>/', single_employee, name='single_employee'),
   path('employees/create/', create_employee, name='create_employee'),
   path('employees/<int:employee_id>/update/', update_employee, name='update_employee'),
   path('employees/<int:employee_id>/delete/', delete_employee, name='delete_employee'),
    
    # Address URLs
   path('addresses/all-addresses', all_addresses, name='all_addresses'),
   path('addresses/<int:address_id>/', single_address, name='single_address'),
   path('addresses/create/', create_address, name='create_address'),
   path('addresses/<int:address_id>/update/', update_address, name='update_address'),
   path('addresses/<int:address_id>/delete/', delete_address, name='delete_address'),
    
    # Project URLs
   path('projects/all-projects', all_projects, name='all_projects'),
   path('projects/<int:project_id>/', single_project, name='single_project'),
   path('projects/create/', create_project, name='create_project'),
   path('projects/<int:project_id>/update/', update_project, name='update_project'),
   path('projects/<int:project_id>/delete/', delete_project, name='delete_project'),
    
    # Task URLs
   path('tasks/all-tasks', all_tasks, name='all_tasks'),
   path('tasks/<int:task_id>/', single_task, name='single_task'),
   path('tasks/create/', create_task, name='create_task'),
   path('tasks/<int:task_id>/update/', update_task, name='update_task'),
   path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
]