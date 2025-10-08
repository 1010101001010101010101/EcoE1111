from django.db import models
from organizations.models import Organization
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AlertRule(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductAlertRule(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    alert_rule = models.ForeignKey(AlertRule, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        # Evita error si product o alert_rule son nulos
        product_name = self.product.name if self.product else "No Product"
        rule_name = self.alert_rule.name if self.alert_rule else "No Rule"
        return f"{product_name} - {rule_name}"


# dispositivos/models.py





class Zone(models.Model):
    name = models.CharField(max_length=120, unique=True)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)  # Relación con organización

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=100)
    serial = models.CharField(max_length=50, unique=True, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='INACTIVE')
    def __str__(self):
        return f"{self.name} ({self.serial})"
    
    def clean(self):
        # Validación para asegurarse de que el dispositivo tenga un producto y una zona
        if not self.product and not self.zone:
            raise ValidationError("El dispositivo debe estar asociado a un producto o una zona.")


class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    unit = models.CharField(max_length=20)

    def __str__(self):
        device_name = self.device.name if self.device else "No Device"
        return f"{device_name}: {self.value} {self.unit}"
