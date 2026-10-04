from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User,
    Tarifa,
    Viaje,
    StaffViaje,
    Producto,
    Envio,
)

# ============================================================
# USER
# ============================================================


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "telefono",
        "ultima_tarifa",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "ultima_tarifa",
    )


# ============================================================
# TARIFA
# ============================================================


@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):

    list_display = (
        "nombre",
        "precio_por_libra",
        "activa",
    )

    list_filter = ("activa",)

    search_fields = ("nombre",)


# ============================================================
# VIAJE
# ============================================================


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "fecha",
        "creado_en",
    )

    list_filter = ("fecha",)


# ============================================================
# STAFF
# ============================================================


@admin.register(StaffViaje)
class StaffViajeAdmin(admin.ModelAdmin):

    list_display = (
        "viaje",
        "usuario",
        "rol",
    )

    list_filter = (
        "rol",
        "viaje",
    )

    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields["usuario"].queryset = User.objects.filter(is_staff=True)

        return form


# ============================================================
# PRODUCTO
# ============================================================


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nombre",
        "cliente",
        "categoria",
        "creado_en",
    )

    list_filter = ("categoria",)

    search_fields = (
        "nombre",
        "cliente__username",
        "cliente__first_name",
        "cliente__last_name",
        "cliente__email",
    )


# ============================================================
# ENVIO
# ============================================================


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "sku",
        "viaje",
        "producto",
        "peso",
        "precio_fijo",
        "extra_fee",
        "monto_total",
        "monto_pagado",
        "estado_entrega",
        "estado_pago",
    )

    list_filter = (
        "estado_entrega",
        "estado_pago",
        "viaje",
    )

    search_fields = (
        "sku",
        "producto__nombre",
        "producto__cliente__username",
        "producto__cliente__first_name",
        "producto__cliente__last_name",
        "producto__cliente__email",
    )

    readonly_fields = (
        "sku",
        "qr_token",
        "monto_total",
        "creado_en",
        "actualizado_en",
    )
