from django.core.management.base import BaseCommand
from accounts.models import Module

class Command(BaseCommand):
    help = "Crea los módulos base del sistema"

    def handle(self, *args, **options):
        modules = [
            {"code": "devices", "name": "Dispositivos", "icon": "cpu"},
            {"code": "zones", "name": "Zonas", "icon": "map"},
            {"code": "alerts", "name": "Alertas", "icon": "bell"},
            {"code": "measurements", "name": "Mediciones", "icon": "bar-chart"},
            {"code": "users", "name": "Usuarios", "icon": "user"},
        ]

        for m in modules:
            obj, created = Module.objects.get_or_create(code=m["code"], defaults=m)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Módulo creado: {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Módulo ya existente: {obj.name}"))

        self.stdout.write(self.style.SUCCESS("🎯 Módulos base creados o actualizados correctamente."))
