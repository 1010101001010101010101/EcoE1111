from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import Role, Module, RoleModulePermission


class Command(BaseCommand):
    help = "Crea roles, módulos y permisos base para EcoEnergy"

    def handle(self, *args, **options):
        ROLES = ['Admin', 'Jefe de Ventas', 'RRHH']
        MODULES = [('ventas', 'Ventas'), ('empleados', 'Empleados')]

        # Crear módulos
        for code, name in MODULES:
            Module.objects.get_or_create(code=code, name=name)

        # Crear grupos y roles
        for role_name in ROLES:
            group, _ = Group.objects.get_or_create(name=role_name)
            Role.objects.get_or_create(group=group)

        # Asignar permisos base
        admin = Role.objects.get(group__name="Admin")
        jefe = Role.objects.get(group__name="Jefe de Ventas")
        rrhh = Role.objects.get(group__name="RRHH")

        ventas = Module.objects.get(code="ventas")
        empleados = Module.objects.get(code="empleados")

        # Admin → todo
        RoleModulePermission.objects.get_or_create(
            role=admin, module=ventas,
            defaults=dict(can_view=True, can_add=True, can_change=True, can_delete=True)
        )
        RoleModulePermission.objects.get_or_create(
            role=admin, module=empleados,
            defaults=dict(can_view=True, can_add=True, can_change=True, can_delete=True)
        )

        # Jefe de Ventas → solo ventas (sin delete)
        RoleModulePermission.objects.get_or_create(
            role=jefe, module=ventas,
            defaults=dict(can_view=True, can_add=True, can_change=True)
        )

        # RRHH → solo empleados (sin delete)
        RoleModulePermission.objects.get_or_create(
            role=rrhh, module=empleados,
            defaults=dict(can_view=True, can_add=True, can_change=True)
        )

        self.stdout.write(self.style.SUCCESS("Roles y módulos creados correctamente ✅"))
