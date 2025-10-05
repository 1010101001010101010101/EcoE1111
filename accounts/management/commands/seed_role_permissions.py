from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import Role, Module, RoleModulePermission


class Command(BaseCommand):
    help = "Asigna permisos base a cada rol según los módulos del sistema"

    def handle(self, *args, **options):
        role_permissions = {
            "Administrador": {"can_view": True, "can_add": True, "can_change": True, "can_delete": True},
            "Supervisor": {"can_view": True, "can_add": True, "can_change": True, "can_delete": False},
            "Operador": {"can_view": True, "can_add": False, "can_change": False, "can_delete": False},
        }

        modules = list(Module.objects.all())
        if not modules:
            self.stdout.write(self.style.ERROR("⚠️ No hay módulos en la BD. Ejecuta primero: python manage.py seed_modules"))
            return

        for role_name, perms in role_permissions.items():
            group, _ = Group.objects.get_or_create(name=role_name)
            role, _ = Role.objects.get_or_create(group=group)

            for module in modules:
                RoleModulePermission.objects.update_or_create(
                    role=role,
                    module=module,
                    defaults=perms
                )
            self.stdout.write(self.style.SUCCESS(f"✅ Permisos asignados a {role_name}"))

        self.stdout.write(self.style.SUCCESS("🎯 Roles y permisos configurados correctamente."))
