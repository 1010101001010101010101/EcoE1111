from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from accounts.models import UserProfile
from organizations.models import Organization

class Command(BaseCommand):
    help = "Crea roles, grupos, organizaciones y usuarios base para pruebas."

    def handle(self, *args, **options):
        # Crear organizaciones base
        org_1, created = Organization.objects.get_or_create(name="Mi empresa")
        org_2, created = Organization.objects.get_or_create(name="Tu empresa")

        if created:
            self.stdout.write(self.style.SUCCESS(f"Organización creada: {org_1.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Organización ya existe: {org_1.name}"))

        if created:
            self.stdout.write(self.style.SUCCESS(f"Organización creada: {org_2.name}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Organización ya existe: {org_2.name}"))

        # Crear grupos (roles)
        roles = ["Cliente - Admin", "Cliente - Electrónico", "EcoEnergy - Admin"]  # Los roles deben existir previamente
        for role_name in roles:
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Grupo creado: {group.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Grupo ya existe: {group.name}"))

        # Crear usuarios para "Mi empresa"
        admin_user, created = User.objects.get_or_create(
            username="admin_mi_empresa",
            email="admin@miempresa.com",
            defaults={"is_staff": True, "is_superuser": True}
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Usuario admin para 'Mi empresa' creado."))

        client_user, created = User.objects.get_or_create(
            username="cliente_mi_empresa",  # Cambié "operador_mi_empresa" por "cliente_mi_empresa"
            email="cliente@miempresa.com",  # Cambié "operador" por "cliente"
            defaults={"is_staff": True, "is_superuser": False}
        )
        if created:
            client_user.set_password("cliente123")
            client_user.save()
            self.stdout.write(self.style.SUCCESS("Usuario cliente para 'Mi empresa' creado."))

        # Crear perfiles para "Mi empresa" con rut único
        admin_profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            organization=org_1,  # Asocia 'Mi empresa'
            rut="11111111-1",  # rut único para evitar duplicados
            telefono="+56911111111",
            direccion="Oficina central, Santiago"
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Perfil de admin para 'Mi empresa' creado."))

        client_profile, created = UserProfile.objects.get_or_create(
            user=client_user,
            organization=org_1,  # Asocia 'Mi empresa'
            rut="22222222-2",  # rut único para evitar duplicados
            telefono="+56922222222",
            direccion="Sucursal norte"
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Perfil de cliente para 'Mi empresa' creado."))

        # Asignar grupos a los usuarios de "Mi empresa"
        admin_group = Group.objects.get(name="Cliente - Admin")
        admin_user.groups.add(admin_group)
        admin_user.save()

        cliente_group = Group.objects.get(name="Cliente - Electrónico")  # Asigné Cliente - Electrónico en vez de Operador
        client_user.groups.add(cliente_group)
        client_user.save()

        self.stdout.write(self.style.SUCCESS("Roles asignados a los usuarios de 'Mi empresa'."))

        # Crear usuarios para "Tu empresa"
        admin_user_2, created = User.objects.get_or_create(
            username="adminTuEmpresa",
            email="admin@tuempresa.com",
            defaults={"is_staff": True, "is_superuser": True}
        )
        if created:
            admin_user_2.set_password("admin123")
            admin_user_2.save()
            self.stdout.write(self.style.SUCCESS("Usuario admin para 'Tu empresa' creado."))

        client_user_2, created = User.objects.get_or_create(
            username="clienteTuEmpresa",  # Cambié "operador_tu_empresa" por "cliente_tu_empresa"
            email="cliente@tuempresa.com",  # Cambié "operador" por "cliente"
            defaults={"is_staff": True, "is_superuser": False}
        )
        if created:
            client_user_2.set_password("cliente123")
            client_user_2.save()
            self.stdout.write(self.style.SUCCESS("Usuario cliente para 'Tu empresa' creado."))

        # Crear perfiles para "Tu empresa" con rut único
        admin_profile_2, created = UserProfile.objects.get_or_create(
            user=admin_user_2,
            organization=org_2,  # Asocia 'Tu empresa'
            rut="33333333-3",
            telefono="+56933333333",
            direccion="Oficina sur, Santiago"
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Perfil de admin para 'Tu empresa' creado."))

        client_profile_2, created = UserProfile.objects.get_or_create(
            user=client_user_2,
            organization=org_2,  # Asocia 'Tu empresa'
            rut="44444444-4",
            telefono="+56944444444",
            direccion="Sucursal sur"
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Perfil de cliente para 'Tu empresa' creado."))

        # Asignar grupos a los usuarios de "Tu empresa"
        admin_group_2 = Group.objects.get(name="Cliente - Admin")
        admin_user_2.groups.add(admin_group_2)
        admin_user_2.save()

        cliente_group_2 = Group.objects.get(name="Cliente - Electrónico")  # Asigné Cliente - Electrónico en vez de Operador
        client_user_2.groups.add(cliente_group_2)
        client_user_2.save()

        self.stdout.write(self.style.SUCCESS("Roles asignados a los usuarios de 'Tu empresa'."))

        self.stdout.write(self.style.SUCCESS("Usuarios, perfiles, roles y organizaciones creados correctamente."))
