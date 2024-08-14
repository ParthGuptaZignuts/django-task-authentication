from django.contrib import admin
from .models import CustomUser,Role,Permission,UserRole,RolePermission

admin.site.register([CustomUser,Role,Permission,UserRole,RolePermission])
