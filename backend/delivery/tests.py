from decimal import Decimal

from django.test import TestCase

from .models import User, Tarifa, Cliente, Viaje, Producto, Envio
from .services import calcular_monto_envio, recalcular_envio


class DeliveryModelTest(TestCase):

    def setUp(self):
        self.tarifa_regular = Tarifa.objects.create(
            nombre="Regular", precio_por_libra=Decimal("10.00")
        )

        self.tarifa_vip = Tarifa.objects.create(
            nombre="VIP", precio_por_libra=Decimal("9.00")
        )

        self.user = User.objects.create_user(
            username="alex", password="123456", first_name="Alex"
        )

        self.cliente = Cliente.objects.create(usuario=self.user)

        self.viaje = Viaje.objects.create(nombre="Viaje de prueba", fecha="2026-09-10")

    def test_producto_regular(self):
        producto = Producto.objects.create(
            nombre="Zapatos", cliente=self.cliente, categoria=Producto.Categoria.REGULAR
        )

        envio = Envio.objects.create(
            viaje=self.viaje,
            producto=producto,
            tarifa=self.tarifa_vip,
            peso=Decimal("5.00"),
            gastos_empresa=Decimal("8.00"),
            extra_fee=Decimal("5.00"),
        )

        total = calcular_monto_envio(envio)

        self.assertEqual(total, Decimal("50.00"))

    def test_producto_electronico(self):
        producto = Producto.objects.create(
            nombre="iPhone",
            cliente=self.cliente,
            categoria=Producto.Categoria.ELECTRONICO,
        )

        envio = Envio.objects.create(
            viaje=self.viaje,
            producto=producto,
            tarifa=self.tarifa_vip,
            peso=Decimal("2.00"),
            precio_fijo=Decimal("35.00"),
            extra_fee=Decimal("5.00"),
        )

        total = calcular_monto_envio(envio)

        self.assertEqual(total, Decimal("40.00"))

    def test_electronico_cuenta_para_peso(self):
        producto = Producto.objects.create(
            nombre="Laptop",
            cliente=self.cliente,
            categoria=Producto.Categoria.ELECTRONICO,
        )

        Envio.objects.create(
            viaje=self.viaje,
            producto=producto,
            tarifa=self.tarifa_vip,
            peso=Decimal("4.00"),
            precio_fijo=Decimal("50.00"),
        )

        self.assertEqual(self.viaje.peso_total, Decimal("4.00"))

    def test_tarifa_pertenece_al_envio(self):
        producto = Producto.objects.create(
            nombre="Zapatos", cliente=self.cliente, categoria=Producto.Categoria.REGULAR
        )

        envio = Envio.objects.create(
            viaje=self.viaje,
            producto=producto,
            tarifa=self.tarifa_vip,
            peso=Decimal("3.00"),
        )

        total = calcular_monto_envio(envio)

        self.assertEqual(total, Decimal("27.00"))

    def test_mismo_producto_en_dos_viajes_con_diferentes_tarifas(self):
        producto = Producto.objects.create(
            nombre="Zapatos", cliente=self.cliente, categoria=Producto.Categoria.REGULAR
        )

        viaje2 = Viaje.objects.create(nombre="Segundo viaje", fecha="2026-09-20")

        # Primer envío
        envio1 = Envio.objects.create(
            viaje=self.viaje,
            producto=producto,
            tarifa=self.tarifa_vip,
            peso=Decimal("5.00"),
            extra_fee=Decimal("5.00"),
            gastos_empresa=Decimal("8.00"),
        )

        # Segundo envío del mismo producto,
        # pero en otro viaje y con otra tarifa
        envio2 = Envio.objects.create(
            viaje=viaje2,
            producto=producto,
            tarifa=self.tarifa_regular,
            peso=Decimal("3.00"),
            extra_fee=Decimal("2.00"),
            gastos_empresa=Decimal("6.00"),
        )

        # Recalculamos ambos envíos
        recalcular_envio(envio1)
        recalcular_envio(envio2)

        # Viaje 1:
        # 5 lb × $9 VIP + $5 extra = $50
        self.assertEqual(envio1.monto_total, Decimal("50.00"))

        # Viaje 2:
        # 3 lb × $10 Regular + $2 extra = $32
        self.assertEqual(envio2.monto_total, Decimal("32.00"))

        # Cada viaje conserva su propio peso
        self.assertEqual(self.viaje.peso_total, Decimal("5.00"))

        self.assertEqual(viaje2.peso_total, Decimal("3.00"))

        # Verificamos que cada envío conserva su propia tarifa
        envio1.refresh_from_db()
        envio2.refresh_from_db()

        self.assertEqual(envio1.tarifa, self.tarifa_vip)

        self.assertEqual(envio2.tarifa, self.tarifa_regular)
