from decimal import Decimal

from django.db import transaction

from .models import Envio


def calcular_monto_envio(envio):
    producto = envio.producto

    if producto.categoria == "REGULAR":
        total = envio.peso * envio.tarifa.precio_por_libra

    elif producto.categoria == "ELECTRONICO":
        total = envio.precio_fijo

    else:
        raise ValueError("Categoría de producto no válida.")

    total += envio.extra_fee

    return total


@transaction.atomic
def recalcular_envio(envio):
    envio.monto_total = calcular_monto_envio(envio)

    envio.save(update_fields=["monto_total", "actualizado_en"])

    return envio


def actualizar_estado_pago(envio):
    if envio.monto_pagado <= Decimal("0.00"):
        envio.estado_pago = Envio.EstadoPago.PENDIENTE

    elif envio.monto_pagado < envio.monto_total:
        envio.estado_pago = Envio.EstadoPago.PARCIAL

    elif envio.monto_pagado == envio.monto_total:
        envio.estado_pago = Envio.EstadoPago.PAGADO

    else:
        raise ValueError("El monto pagado no puede ser mayor que el monto total.")

    envio.save(update_fields=["estado_pago", "actualizado_en"])

    return envio
