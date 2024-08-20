from django.db import models

class Company(models.Model):
    company_name        = models.CharField(max_length=50)
    company_description = models.TextField(blank=True)
    company_website     = models.URLField(blank=True, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

class Department(models.Model):
    company         = models.ForeignKey(Company, related_name="departments", on_delete=models.CASCADE)
    department_name = models.CharField(max_length=50)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department_name

class Employee(models.Model):
    first_name   = models.CharField(max_length=255)  
    last_name    = models.CharField(max_length=255) 
    email        = models.EmailField(unique=True)
    company      = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    department   = models.ForeignKey(Department, related_name='employees', on_delete=models.SET_NULL, null=True, blank=True)
    hire_date    = models.DateField() 

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address(models.Model):
    company = models.OneToOneField(Company, related_name='address', on_delete=models.CASCADE)
    street  = models.CharField(max_length=255)  
    city    = models.CharField(max_length=255)  
    state   = models.CharField(max_length=255)  
    country = models.CharField(max_length=255) 

    def __str__(self):
        return f"{self.street}, {self.city}" 

class Project(models.Model):
    company     = models.ForeignKey(Company, related_name='projects', on_delete=models.CASCADE)
    name        = models.CharField(max_length=255)  
    description = models.TextField(blank=True) 
    start_date  = models.DateField() 
    end_date    = models.DateField(null=True, blank=True) 
    employees   = models.ManyToManyField(Employee, related_name='projects')

    def __str__(self):
        return self.name
    
class Task(models.Model):
    employee    = models.ForeignKey(Employee, related_name='tasks', on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)  
    description = models.TextField(blank=True)  
    due_date    = models.DateField() 
    completed   = models.BooleanField(default=False) 

    def __str__(self):
        return self.title
