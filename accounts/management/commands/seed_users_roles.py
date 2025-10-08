from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction
from accounts.models import Role, RoleModulePermission  # Ajusta a tu app

class Command(BaseCommand):
    help = "Siembra usuarios y roles en el sistema."

    @transaction.atomic
    def handle(self, *args, **options):
        # Crear los usuarios
        self.create_users()

        # Crear roles y asignar permisos
        self.create_roles_and_permissions()

    def create_users(self):
        # Crear un superusuario
        superuser, created = User.objects.get_or_create(
            username="admin", email="admin@example.com"
        )
        if created:
            superuser.set_password("adminpassword")
            superuser.is_superuser = True
            superuser.is_staff = True
            superuser.save()

        # Crear un usuario con un rol limitado
        limited_user, created = User.objects.get_or_create(
            username="cliente_electronico", email="cliente@example.com"
        )
        if created:
            limited_user.set_password("cliente123")
            limited_user.save()

        self.stdout.write(self.style.SUCCESS("Usuarios creados correctamente."))

    def create_roles_and_permissions(self):
        # Crear roles (grupos)
        group_admin, created = Group.objects.get_or_create(name="EcoEnergy - Admin")
        group_cliente, created = Group.objects.get_or_create(name="Cliente - Electrónico")

        # Asignar roles a los usuarios
        admin_user = User.objects.get(username="admin")
        cliente_user = User.objects.get(username="cliente_electronico")

        admin_user.groups.add(group_admin)
        cliente_user.groups.add(group_cliente)

        # Crear y asignar permisos a los roles
        self.create_permissions_for_role(group_admin, "all")
        self.create_permissions_for_role(group_cliente, "view")

        self.stdout.write(self.style.SUCCESS("Roles y permisos asignados correctamente."))

    def create_permissions_for_role(self, group, actions):
        """Crea permisos asociados a un rol específico."""
        modules = ["operacion", "accounts", "organizations"]
        if actions == "all":
            actions = ["view", "add", "change", "delete"]
        else:
            actions = [actions]  # Solo permitir la acción especificada

        for module in modules:
            for action in actions:
                permission_codename = f"{action}_{module}"
                # Si el permiso no existe, crearlo
                perm, created = RoleModulePermission.objects.get_or_create(
                    role=Role.objects.get(group=group),
                    module_code=module,
                    action=action
                )

        self.stdout.write(self.style.SUCCESS(f"Permisos para el grupo {group.name} asignados correctamente."))
