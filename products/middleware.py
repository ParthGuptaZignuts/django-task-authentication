from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from permissions.models import UserRole, RolePermission

class ModulePermissionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/api/products/'):
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            token = auth_header.replace('Token ', '').strip() if auth_header else None
            
            if token:
                try:
                    token_obj = Token.objects.get(key=token)
                    request.user = token_obj.user
                except Token.DoesNotExist:
                    print("Invalid token")
                    return HttpResponse('Unauthorized', status=401)
            else:
                print("No token provided")
                return HttpResponse('Unauthorized', status=401)
            
            if not request.user.is_authenticated:
                print("User not authenticated")
                return HttpResponse('Unauthorized', status=401)
            
            if request.user.is_superuser:
                return None
            
            username = request.user.username if hasattr(request.user, 'username') else 'No username'
            print(f"Authenticated user: {username}")

            module_name = 'products'
            user_roles = UserRole.objects.filter(user=request.user)
            role_ids = [role.role.id for role in user_roles]
            user_permissions = RolePermission.objects.filter(role__in=role_ids)
            
            allowed_permissions = [perm.permission.permission for perm in user_permissions if perm.permission.module == module_name]
            
            print(f"User authenticated: {request.user.is_authenticated}")
            print(f"User roles: {[role.role.name for role in user_roles]}")
            print(f"User permissions: {[perm.permission.permission for perm in user_permissions]}")
            print(f"Allowed permissions: {allowed_permissions}")

            method = request.method.lower()
            if method in ['get', 'post', 'put', 'delete']:
                if method not in allowed_permissions:
                    print(f"Permission denied for method: {method}")
                    return HttpResponse('Forbidden', status=403)
        
        return None
