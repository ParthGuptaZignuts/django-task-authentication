from rest_framework import serializers
from .models import Company, Department, Employee, Address, Project, Task

class CompanySerializer(serializers.ModelSerializer):
    departments = serializers.StringRelatedField(many=True)
    employees   = serializers.StringRelatedField(many=True)
    address     = serializers.StringRelatedField()
    projects    = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    employees = serializers.StringRelatedField(many=True)

    class Meta:
        model = Department
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    company    = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    projects   = serializers.StringRelatedField(many=True)
    tasks      = serializers.StringRelatedField(many=True)

    class Meta:
        model = Employee
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Address
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    company   = serializers.StringRelatedField()  
    employees = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField() 

    class Meta:
        model = Task
        fields = '__all__'
