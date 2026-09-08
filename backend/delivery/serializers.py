from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import (
    Tarifa,
    Cliente,
    Viaje,
    StaffViaje,
    Producto,
    Envio,
)

from .services import (
    recalcular_envio,
    actualizar_estado_pago,
)

User = get_user_model()


# ============================================================
# USER
# ============================================================


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "telefono",
            "ultima_tarifa",
        ]

        read_only_fields = [
            "id",
        ]


# ============================================================
# TARIFA
# ============================================================


class TarifaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tarifa

        fields = [
            "id",
            "nombre",
            "precio_por_libra",
            "activa",
        ]

        read_only_fields = [
            "id",
        ]

    def validate_precio_por_libra(self, value):

        if value <= Decimal("0.00"):
            raise serializers.ValidationError(
                "El precio por libra debe ser mayor que cero."
            )

        return value


# ============================================================
# CLIENTE
# ============================================================


class ClienteSerializer(serializers.ModelSerializer):

    usuario = UserSerializer()

    class Meta:
        model = Cliente

        fields = [
            "id",
            "usuario",
            "activo",
        ]

        read_only_fields = [
            "id",
        ]


# ============================================================
# VIAJE
# ============================================================


class ViajeSerializer(serializers.ModelSerializer):

    peso_total = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    ingresos_totales = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    gastos_totales = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    ganancia = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Viaje

        fields = [
            "id",
            "nombre",
            "fecha",
            "creado_en",
            "peso_total",
            "ingresos_totales",
            "gastos_totales",
            "ganancia",
        ]

        read_only_fields = [
            "id",
            "creado_en",
            "peso_total",
            "ingresos_totales",
            "gastos_totales",
            "ganancia",
        ]


# ============================================================
# STAFF DEL VIAJE
# ============================================================


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffViaje

        fields = [
            "id",
            "viaje",
            "usuario",
            "rol",
        ]

        read_only_fields = [
            "id",
        ]


# ============================================================
# PRODUCTO
# ============================================================


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto

        fields = [
            "id",
            "nombre",
            "cliente",
            "descripcion",
            "categoria",
            "creado_en",
        ]

        read_only_fields = [
            "id",
            "creado_en",
        ]


# ============================================================
# ENVIO
# ============================================================


class EnvioSerializer(serializers.ModelSerializer):

    cliente = serializers.IntegerField(source="producto.cliente_id", read_only=True)

    class Meta:
        model = Envio

        fields = [
            "id",
            "viaje",
            "producto",
            "cliente",
            "sku",
            "qr_token",
            "peso",
            "tarifa",
            "gastos_empresa",
            "extra_fee",
            "precio_fijo",
            "estado_entrega",
            "estado_pago",
            "monto_total",
            "monto_pagado",
            "creado_en",
            "actualizado_en",
        ]

        read_only_fields = [
            "id",
            "sku",
            "qr_token",
            "cliente",
            "monto_total",
            "creado_en",
            "actualizado_en",
        ]

    def validate(self, attrs):

        viaje = attrs.get("viaje", getattr(self.instance, "viaje", None))

        producto = attrs.get("producto", getattr(self.instance, "producto", None))

        if not viaje or not producto:
            return attrs

        if not producto.cliente.activo:
            raise serializers.ValidationError("El cliente está inactivo.")

        peso = attrs.get("peso", getattr(self.instance, "peso", None))

        if peso is not None and peso <= Decimal("0.00"):
            raise serializers.ValidationError("El peso debe ser mayor que cero.")

        tarifa = attrs.get("tarifa", getattr(self.instance, "tarifa", None))

        if tarifa and not tarifa.activa:
            raise serializers.ValidationError("La tarifa seleccionada está inactiva.")

        precio_fijo = attrs.get(
            "precio_fijo", getattr(self.instance, "precio_fijo", Decimal("0.00"))
        )

        if producto.categoria == Producto.Categoria.ELECTRONICO:

            if precio_fijo <= Decimal("0.00"):
                raise serializers.ValidationError(
                    "Los productos electrónicos deben tener "
                    "un precio fijo mayor que cero."
                )

        elif producto.categoria == Producto.Categoria.REGULAR:

            if precio_fijo != Decimal("0.00"):
                raise serializers.ValidationError(
                    "Los productos regulares no utilizan " "precio fijo."
                )

        extra_fee = attrs.get(
            "extra_fee", getattr(self.instance, "extra_fee", Decimal("0.00"))
        )

        if extra_fee < Decimal("0.00"):
            raise serializers.ValidationError("El extra fee no puede ser negativo.")

        return attrs

    def create(self, validated_data):

        envio = Envio.objects.create(**validated_data)

        recalcular_envio(envio)

        return envio

    def update(self, instance, validated_data):

        instance = super().update(instance, validated_data)

        recalcular_envio(instance)

        return instance
