from django.contrib import admin
from .models import Category, Product, Device, Measurement, AlertRule, ProductAlertRule
from django.core.exceptions import ValidationError

# Acción personalizada
@admin.action(description="Activar dispositivos seleccionados")
def make_active(modeladmin, request, queryset):
    queryset.update(status="ACTIVE")

@admin.action(description="Desactivar dispositivos seleccionados")
def make_inactive(modeladmin, request, queryset):
    queryset.update(status="INACTIVE")

# Personalización general del Admin
admin.site.site_header = "EcoEnergy — Admin"
admin.site.site_title = "EcoEnergy Admin"
admin.site.index_title = "Panel de administración"

# Registros del Admin para modelos
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 50


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category")
    search_fields = ("name", "sku", "category__name")
    list_filter = ("category",)
    ordering = ("name",)
    list_select_related = ("category",)
    list_per_page = 50


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "min_value", "max_value")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 50


@admin.register(ProductAlertRule)
class ProductAlertRuleAdmin(admin.ModelAdmin):
    list_display = ("product", "alert_rule")
    list_filter = ("product", "alert_rule")
    ordering = ("product",)
    list_select_related = ("product", "alert_rule")
    list_per_page = 50


# ─────────────────────────────
# POR ORGANIZACIÓN
# ─────────────────────────────
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "serial", "status", "product", "zone", "organization")
    search_fields = ("name", "serial", "product__name", "zone__name", "organization__name")
    list_filter = ("organization", "zone", "product", "status")
    ordering = ("organization", "zone")
    list_select_related = ("product", "zone", "organization")
    list_per_page = 50
    actions = [make_active, make_inactive]

    # Scoping por organización
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.userprofile.organization)

    # Limitar Zonas y Productos al crear
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "zone" or db_field.name == "organization":
            # Importamos Zone solo cuando sea necesario para evitar ciclo de importación
            from dispositivos.models import Zone
            if not request.user.is_superuser:
                kwargs["queryset"] = kwargs["queryset"].filter(
                    organization=request.user.userprofile.organization
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Validación en el modelo (Device)
    def clean(self):
        # Validación para asegurarse de que el dispositivo tenga un producto y una zona
        if not self.product and not self.zone:
            raise ValidationError("El dispositivo debe estar asociado a un producto o una zona.")
        super().clean()


# ─────────────────────────────
# SERIES (lecturas)
# ─────────────────────────────
@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ("device", "timestamp", "value", "unit")
    list_filter = ("device",)
    search_fields = ("device__name",)
    ordering = ("-timestamp",)
    list_select_related = ("device",)
    list_per_page = 50

    # Scoping por organización
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(device__organization=request.user.userprofile.organization)
