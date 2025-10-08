from django.contrib import admin
from .models import UserProfile, Module, Role, RoleModulePermission


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "organization",  "rut", "telefono")
    #list_filter = ("organization")
    search_fields = ("user__username", "rut", "organization__name")
    ordering = ("organization", "user")
    autocomplete_fields = ("organization",)
    list_select_related = ("organization", "user")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "icon")
    search_fields = ("name", "code")
    ordering = ("name",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("group",)
    search_fields = ("group__name",)
    ordering = ("group",)


@admin.register(RoleModulePermission)
class RoleModulePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "module", "can_view", "can_add", "can_change", "can_delete")
    list_filter = ("role", "module")
    search_fields = ("role__group__name", "module__name")
    ordering = ("role", "module")
    list_select_related = ("role", "module")
