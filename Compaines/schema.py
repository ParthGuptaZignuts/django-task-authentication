import graphene
from graphene_django import DjangoObjectType
from .models import Company, Department, Employee, Address, Project, Task

class CompanyType(DjangoObjectType):
    class Meta:
        model = Company

class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department

class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee

class AddressType(DjangoObjectType):
    class Meta:
        model = Address

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project

class TaskType(DjangoObjectType):
    class Meta:
        model = Task

class Query(graphene.ObjectType):
    all_companies = graphene.List(CompanyType)
    company       = graphene.Field(CompanyType, id=graphene.Int())
    
    all_departments = graphene.List(DepartmentType)
    department      = graphene.Field(DepartmentType, id=graphene.Int())

    all_employees = graphene.List(EmployeeType)
    employee      = graphene.Field(EmployeeType, id=graphene.Int())

    all_addresses = graphene.List(AddressType)
    address       = graphene.Field(AddressType, id=graphene.Int())

    all_projects = graphene.List(ProjectType)
    project      = graphene.Field(ProjectType, id=graphene.Int())

    all_tasks = graphene.List(TaskType)
    task      = graphene.Field(TaskType, id=graphene.Int())

    def resolve_all_companies(self, info):
        return Company.objects.all()

    def resolve_company(self, info, id):
        return Company.objects.get(id=id)

    def resolve_all_departments(self, info):
        return Department.objects.all()

    def resolve_department(self, info, id):
        return Department.objects.get(id=id)

    def resolve_all_employees(self, info):
        return Employee.objects.all()

    def resolve_employee(self, info, id):
        return Employee.objects.get(id=id)

    def resolve_all_addresses(self, info):
        return Address.objects.all()

    def resolve_address(self, info, id):
        return Address.objects.get(id=id)

    def resolve_all_projects(self, info):
        return Project.objects.all()

    def resolve_project(self, info, id):
        return Project.objects.get(id=id)

    def resolve_all_tasks(self, info):
        return Task.objects.all()

    def resolve_task(self, info, id):
        return Task.objects.get(id=id)

schema = graphene.Schema(query=Query)