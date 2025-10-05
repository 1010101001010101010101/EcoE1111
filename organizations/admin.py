from django.contrib import admin
from .models import Organization
from dispositivos.models import Zone  # Hijo (de otra app)
from .forms import OrganizationForm
# ─────────────────────────────
# INLINE — Zones dentro de Organization
# ─────────────────────────────
class ZoneInline(admin.TabularInline):
    model = Zone
    extra = 0
    fields = ("name",)
    show_change_link = True
   

# ─────────────────────────────
# ORGANIZATION ADMIN
# ─────────────────────────────
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationForm
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [ZoneInline]           # ¡Aquí conectas el inline!
