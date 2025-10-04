from django.contrib import admin
from .models import Category, Product, Zone, Device, Measurement, AlertRule, ProductAlertRule

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category")
    list_filter = ("category",)
    search_fields = ("name", "sku")


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "organization")
    list_filter = ("organization",)
    search_fields = ("name",)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "serial", "product", "zone", "organization")
    list_filter = ("organization", "zone")
    search_fields = ("name", "serial")


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("device", "timestamp", "value", "unit")
    list_filter = ("device",)
    search_fields = ("device__name",)


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "min_value", "max_value")
    search_fields = ("name",)


@admin.register(ProductAlertRule)
class ProductAlertRuleAdmin(admin.ModelAdmin):
    list_display = ("product", "alert_rule")
    list_filter = ("product",)
