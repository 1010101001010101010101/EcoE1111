from django.core.management.base import BaseCommand
from dispositivos.models import Category, Product, AlertRule, ProductAlertRule, Zone, Device, Measurement
from organizations.models import Organization
from random import randint
from django.utils import timezone

class Command(BaseCommand):
    help = "Crea organizaciones, zonas, productos, dispositivos, mediciones y reglas de alerta."

    def handle(self, *args, **options):
        # Crear zonas
        zone_norte, created = Zone.objects.get_or_create(name="Zona Norte")
        zone_sur, created = Zone.objects.get_or_create(name="Zona Sur")
        zone_central, created = Zone.objects.get_or_create(name="Zona Central")

        self.stdout.write(self.style.SUCCESS(f"Zonas creadas: {zone_norte.name}, {zone_sur.name}, {zone_central.name}"))

        # Crear organizaciones
        org_tu_empresa, created = Organization.objects.get_or_create(name="Tu empresa")
        org_mi_empresa, created = Organization.objects.get_or_create(name="Mi empresa")
        org_nuestra_empresa, created = Organization.objects.get_or_create(name="Nuestra empresa")

        self.stdout.write(self.style.SUCCESS(f"Organizaciones creadas: {org_tu_empresa.name}, {org_mi_empresa.name}, {org_nuestra_empresa.name}"))

        # Asignar zonas a las organizaciones (usa `zones.add()` porque es una relación ManyToMany)
        org_mi_empresa.zones.add(zone_norte)
        org_tu_empresa.zones.add(zone_sur)
        org_nuestra_empresa.zones.add(zone_central)

        self.stdout.write(self.style.SUCCESS(f"Zonas asignadas a las organizaciones exitosamente"))

        # Crear categorías de productos
        categories = ["Electrónica", "Mecánica", "Hogar", "Oficina"]
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Categoría creada: {category.name}"))

        # Crear productos
        products = [
            {"name": "Smartphone", "sku": "SKU001", "category": Category.objects.first()},
            {"name": "Laptop", "sku": "SKU002", "category": Category.objects.first()},
            {"name": "Silla", "sku": "SKU003", "category": Category.objects.first()},
            {"name": "Escritorio", "sku": "SKU004", "category": Category.objects.first()},
        ]
        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Producto creado: {product.name}"))
                # Crear dispositivos asociados a los productos
                self.create_device_for_product(product)
                # Crear reglas de alerta para el producto
                self.create_alert_rules_for_product(product)

        # Crear reglas de alerta
        alert_rules = [
            {"name": "Temperatura alta", "min_value": 30, "max_value": 70},
            {"name": "Temperatura baja", "min_value": -10, "max_value": 10},
            {"name": "Humedad alta", "min_value": 60, "max_value": 100},
        ]
        for alert_rule in alert_rules:
            rule, created = AlertRule.objects.get_or_create(**alert_rule)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Regla de alerta creada: {rule.name}"))

        self.stdout.write(self.style.SUCCESS("Semilla de datos creada con éxito."))

    def create_device_for_product(self, product):
        """Crea un dispositivo asociado a un producto."""
        zone = Zone.objects.first()  # Asociar con la primera zona disponible
        device_name = f"Dispositivo {product.name}"  # Nombre del dispositivo basado en el producto
        serial = f"SN_{randint(1000, 9999)}"  # Serial aleatorio para el dispositivo

        # Crear el dispositivo asociado al producto
        device, created = Device.objects.get_or_create(
            name=device_name, 
            serial=serial, 
            product=product, 
            zone=zone, 
            organization=None  # Puedes asociar la organización según sea necesario
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Dispositivo creado: {device.name}"))
            # Crear mediciones para el dispositivo
            self.create_measurements_for_device(device)

    def create_measurements_for_device(self, device):
        """Crea mediciones para un dispositivo."""
        for _ in range(3):  # Crear 3 mediciones por dispositivo
            value = randint(1, 100)  # Valor aleatorio
            unit = "Celsius" if randint(0, 1) == 0 else "Percentage"  # Aleatorio entre temperatura y porcentaje
            timestamp = timezone.now()

            measurement = Measurement.objects.create(
                device=device,
                value=value,
                unit=unit,
                timestamp=timestamp
            )
            self.stdout.write(self.style.SUCCESS(f"Medición creada: {measurement.value} {measurement.unit} para {device.name}"))

    def create_alert_rules_for_product(self, product):
        """Crea reglas de alerta para un producto y lo asocia con el producto."""
        for alert_rule in AlertRule.objects.all():
            # Crear la relación entre el producto y las reglas de alerta
            product_alert_rule, created = ProductAlertRule.objects.get_or_create(
                product=product,
                alert_rule=alert_rule
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Regla de alerta {alert_rule.name} asociada a producto {product.name}"))
