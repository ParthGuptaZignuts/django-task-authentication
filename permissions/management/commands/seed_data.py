from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from permissions.models import CustomUser, Role, Permission, UserRole, RolePermission

class Command(BaseCommand):
    help = 'Seed the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        roles = ['Admin', 'Editor', 'Viewer']
        for role_name in roles:
            Role.objects.get_or_create(name=role_name)

        permissions = ['get', 'post', 'put', 'delete']
        modules = ['user', 'role', 'permission']
        for module in modules:
            for perm in permissions:
                Permission.objects.get_or_create(module=module, permission=perm)

        for _ in range(10):
            user = CustomUser.objects.create_user(
                email=fake.email(),
                password=fake.password(),
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_staff=fake.boolean(chance_of_getting_true=50),
                is_active=fake.boolean(chance_of_getting_true=50),
            )

            roles = Role.objects.all()
            if roles:
                assigned_roles = roles.order_by('?')[:2]  
                for role in assigned_roles:
                    UserRole.objects.get_or_create(user=user, role=role)

                for role in assigned_roles:
                    permissions = Permission.objects.all()
                    if permissions:
                        assigned_permissions = permissions.order_by('?')[:3] 
                        for permission in assigned_permissions:
                            RolePermission.objects.get_or_create(role=role, permission=permission)

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with fake data'))
