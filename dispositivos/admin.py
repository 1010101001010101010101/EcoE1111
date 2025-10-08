from django.contrib import admin
from .models import Category, Product, Zone, Device, Measurement, AlertRule, ProductAlertRule

# ─────────────────────────────
# ACCIONES PERSONALIZADAS
# ─────────────────────────────
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

# ─────────────────────────────
# MAESTROS (Globales)
# ─────────────────────────────
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
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "organization")
    search_fields = ("name", "organization__name")
    list_filter = ("organization",)
    ordering = ("organization", "name")
    list_select_related = ("organization",)
    list_per_page = 50

    # Scoping por organización
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.userprofile.organization)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization" and not request.user.is_superuser:
            kwargs["queryset"] = kwargs["queryset"].filter(
                id=request.user.userprofile.organization.id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "serial", "product", "zone", "organization")
    search_fields = ("name", "serial", "product__name", "zone__name", "organization__name")
    list_filter = ("organization", "zone", "product")
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
        if not request.user.is_superuser:
            if db_field.name == "zone":
                kwargs["queryset"] = kwargs["queryset"].filter(
                    organization=request.user.userprofile.organization
                )
            elif db_field.name == "organization":
                kwargs["queryset"] = kwargs["queryset"].filter(
                    id=request.user.userprofile.organization.id
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
