import uuid
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models

# ============================================================
# TARIFAS
# ============================================================


class Tarifa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    precio_por_libra = models.DecimalField(max_digits=10, decimal_places=2)

    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} - ${self.precio_por_libra}/lb"


# ============================================================
# USUARIO
# ============================================================


class User(AbstractUser):

    telefono = models.CharField(max_length=30, blank=True)

    # Última tarifa utilizada por el usuario.
    #
    # IMPORTANTE:
    # Esto NO representa el historial de tarifas.
    # Solo sirve para sugerir una tarifa cuando se
    # agregue nuevamente al cliente a un viaje.
    ultima_tarifa = models.ForeignKey(
        Tarifa,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="usuarios_ultima_tarifa",
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username


# ============================================================
# CLIENTE
# ============================================================


class Cliente(models.Model):

    usuario = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="cliente"
    )

    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username


# ============================================================
# VIAJE
# ============================================================


class Viaje(models.Model):

    nombre = models.CharField(max_length=150, blank=True)

    fecha = models.DateField()

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Viaje"
        verbose_name_plural = "Viajes"
        ordering = ["-fecha", "-id"]

    def __str__(self):

        if self.nombre:
            return f"{self.nombre} - {self.fecha}"

        return f"Viaje #{self.id} - {self.fecha}"

    @property
    def peso_total(self):
        """
        Peso total de todos los envíos del viaje.

        Incluye:
        - productos regulares
        - productos electrónicos

        Aunque los electrónicos se cobran por precio fijo,
        su peso SI cuenta para el peso total del viaje.
        """

        return sum((envio.peso for envio in self.envios.all()), Decimal("0.00"))

    @property
    def ingresos_totales(self):
        """
        Total cobrado a los clientes en este viaje.
        """

        return sum((envio.monto_total for envio in self.envios.all()), Decimal("0.00"))

    @property
    def gastos_totales(self):
        """
        Gastos de empresa de todos los envíos
        pertenecientes a este viaje.
        """

        return sum(
            (envio.gastos_empresa for envio in self.envios.all()), Decimal("0.00")
        )

    @property
    def ganancia(self):
        """
        Ganancia = ingresos - gastos.
        """

        return self.ingresos_totales - self.gastos_totales


# ============================================================
# Staff del Viaje
# ============================================================


class StaffViaje(models.Model):

    class Rol(models.TextChoices):
        EMPACADOR = "EMPACADOR", "Empacador"
        VIAJERO = "VIAJERO", "Viajero"
        DISTRIBUIDOR = "DISTRIBUIDOR", "Distribuidor"
        REPARTIDOR = "REPARTIDOR", "Repartidor"

    viaje = models.ForeignKey(Viaje, on_delete=models.PROTECT, related_name="staff")

    usuario = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="staff_viajes"
    )

    rol = models.CharField(max_length=20, choices=Rol.choices)

    class Meta:
        verbose_name = "Staff del Viaje"
        verbose_name_plural = "Staff del Viaje"

        constraints = [
            models.UniqueConstraint(
                fields=["viaje", "usuario", "rol"], name="unique_usuario_rol_viaje"
            )
        ]

    def __str__(self):
        return f"{self.usuario} - " f"{self.rol} - " f"{self.viaje}"


# ============================================================
# PRODUCTO
# ============================================================


class Producto(models.Model):

    class Categoria(models.TextChoices):
        REGULAR = "REGULAR", "Regular"
        ELECTRONICO = "ELECTRONICO", "Electrónico"

    nombre = models.CharField(max_length=200)

    cliente = models.ForeignKey(
        Cliente, on_delete=models.PROTECT, related_name="productos"
    )

    descripcion = models.TextField(blank=True)

    categoria = models.CharField(
        max_length=20, choices=Categoria.choices, default=Categoria.REGULAR
    )

    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.nombre} - " f"{self.cliente}"


# ============================================================
# ENVÍO
# ============================================================


class Envio(models.Model):

    # --------------------------------------------------------
    # ESTADO DE ENTREGA
    # --------------------------------------------------------

    class EstadoEntrega(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ENVIADO = "ENVIADO", "Enviado"
        RECIBIDO = "RECIBIDO", "Recibido"
        ENTREGADO = "ENTREGADO", "Entregado"

    # --------------------------------------------------------
    # ESTADO DE PAGO
    # --------------------------------------------------------

    class EstadoPago(models.TextChoices):
        PAGADO = "PAGADO", "Pagado"
        PARCIAL = "PARCIAL", "Pago parcial"
        PENDIENTE = "PENDIENTE", "Pendiente de pago"
        CREDITO = "CREDITO", "Crédito del cliente"

    # --------------------------------------------------------
    # RELACIONES
    # --------------------------------------------------------

    viaje = models.ForeignKey(Viaje, on_delete=models.PROTECT, related_name="envios")

    producto = models.ForeignKey(
        Producto, on_delete=models.PROTECT, related_name="envios"
    )
    tarifa = models.ForeignKey(Tarifa, on_delete=models.PROTECT, related_name="envios")
    # --------------------------------------------------------
    # IDENTIFICACIÓN
    # --------------------------------------------------------

    # El SKU pertenece al envío.
    #
    # El mismo producto puede tener diferentes SKU
    # en diferentes viajes.
    sku = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
    )

    # Token único utilizado para identificar
    # este envío mediante QR.
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # --------------------------------------------------------
    # INFORMACIÓN DEL PRODUCTO EN ESTE VIAJE
    # --------------------------------------------------------

    # Este peso pertenece al envío.
    #
    # Puede cambiar de un viaje a otro.
    peso = models.DecimalField(max_digits=10, decimal_places=2)

    # Gasto particular de la empresa
    # para este envío en este viaje.
    gastos_empresa = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    # Cargo adicional del envío.
    #
    # Ejemplos:
    # - Personal shopper
    # - Uso de tarjeta
    # - Servicio adicional
    extra_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    # --------------------------------------------------------
    # PRECIO FIJO PARA ELECTRÓNICOS
    # --------------------------------------------------------

    # Para productos ELECTRÓNICOS:
    #
    #     monto = precio_fijo + extra_fee
    #
    # El peso NO participa en el cálculo del precio,
    # pero SI cuenta para el peso total del viaje.
    #
    # Para productos REGULARES este campo puede ser 0.
    precio_fijo = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    # --------------------------------------------------------
    # ESTADOS
    # --------------------------------------------------------

    estado_entrega = models.CharField(
        max_length=20, choices=EstadoEntrega.choices, default=EstadoEntrega.PENDIENTE
    )

    estado_pago = models.CharField(
        max_length=20, choices=EstadoPago.choices, default=EstadoPago.PENDIENTE
    )

    # --------------------------------------------------------
    # INFORMACIÓN ECONÓMICA
    # --------------------------------------------------------

    monto_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    monto_pagado = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )

    # --------------------------------------------------------
    # FECHAS
    # --------------------------------------------------------

    creado_en = models.DateTimeField(auto_now_add=True)

    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Envío"
        verbose_name_plural = "Envíos"

        constraints = [
            models.UniqueConstraint(
                fields=["viaje", "producto"], name="unique_producto_por_viaje"
            )
        ]

        ordering = ["-id"]

    def __str__(self):
        return f"{self.sku} - " f"{self.producto.nombre}"

    def save(self, *args, **kwargs):
        if not self.sku:
            # Primero necesitamos el ID del envío.
            # Usamos temporalmente un SKU único para poder guardar.
            self.sku = f"TEMP-{uuid.uuid4()}"

            super().save(*args, **kwargs)

            # Ahora que tenemos el ID podemos generar
            # el SKU definitivo.
            self.sku = f"GLZ-{self.viaje_id}-{self.id:06d}"

            super().save(update_fields=["sku"])

            return

        super().save(*args, **kwargs)
