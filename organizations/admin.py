from django.contrib import admin
from .models import Organization
from dispositivos.models import Zone
from .forms import OrganizationForm

# ─────────────────────────────
# INLINE — Zonas dentro de Organization
# ─────────────────────────────
class ZoneInline(admin.TabularInline):
    model = Zone
    extra = 0
    fields = ("name",)
    show_change_link = True

    # Evitar error de admin.E201 (no excluir el FK organization)
    can_delete = False

    # Scoping: solo mostrar zonas de la organización del usuario
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.userprofile.organization)


# ─────────────────────────────
# ORGANIZATION ADMIN
# ─────────────────────────────
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    form = OrganizationForm
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    inlines = [ZoneInline]

    # Scoping: limitar visualización por organización
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.userprofile.organization.id)

    # Impedir ver/editar organizaciones ajenas
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.id != request.user.userprofile.organization.id:
            return False
        return True

    # Impedir eliminar organizaciones ajenas
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.id == request.user.userprofile.organization.id:
            return True
        return False

    # Evitar que usuarios comunes creen nuevas organizaciones
    def has_add_permission(self, request):
        return request.user.is_superuser
