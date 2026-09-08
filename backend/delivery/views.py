from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import StaffViaje
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import (
    EsAdministrador,
    EsStaff,
    EsRepartidorDelViaje,
    EsCliente,
    EsPropietarioDelEnvio,
)

from django.contrib.auth import get_user_model

from .models import (
    StaffViaje,
    Tarifa,
    Cliente,
    Viaje,
    Producto,
    Envio,
)

from .serializers import (
    StaffSerializer,
    UserSerializer,
    TarifaSerializer,
    ClienteSerializer,
    ViajeSerializer,
    StaffSerializer,
    ProductoSerializer,
    EnvioSerializer,
)

User = get_user_model()


# ============================================================
# USERS
# ============================================================


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# TARIFAS
# ============================================================


class TarifaViewSet(viewsets.ModelViewSet):

    queryset = Tarifa.objects.all()

    serializer_class = TarifaSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# CLIENTES
# ============================================================


class ClienteViewSet(viewsets.ModelViewSet):

    queryset = Cliente.objects.select_related("usuario").all()

    serializer_class = ClienteSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# VIAJES
# ============================================================


class ViajeViewSet(viewsets.ModelViewSet):

    queryset = Viaje.objects.all()

    serializer_class = ViajeSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# STAFF
# ============================================================


class StaffViewSet(viewsets.ModelViewSet):

    queryset = StaffViaje.objects.select_related("viaje", "usuario").all()

    serializer_class = StaffSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# PRODUCTOS
# ============================================================


class ProductoViewSet(viewsets.ModelViewSet):

    queryset = Producto.objects.select_related("cliente", "cliente__usuario").all()

    serializer_class = ProductoSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# ENVIOS
# ============================================================


class EnvioViewSet(viewsets.ModelViewSet):
    queryset = Envio.objects.select_related(
        "viaje",
        "producto",
        "producto__cliente",
        "producto__cliente__usuario",
    ).all()

    serializer_class = EnvioSerializer

    def get_permissions(self):

        # ADMINISTRADOR
        if self.request.user.is_superuser:
            return [EsAdministrador()]

        # CLIENTE
        if hasattr(self.request.user, "cliente"):
            return [EsCliente()]

        # STAFF
        if StaffViaje.objects.filter(usuario=self.request.user).exists():
            return [EsStaff()]

        return [IsAuthenticated()]

    def get_queryset(self):

        user = self.request.user

        # SUPERUSUARIO
        if user.is_superuser:
            return self.queryset

        # CLIENTE
        if hasattr(user, "cliente"):
            return self.queryset.filter(producto__cliente__usuario=user)

        # STAFF
        viajes_staff = StaffViaje.objects.filter(usuario=user).values_list(
            "viaje_id", flat=True
        )

        return self.queryset.filter(viaje_id__in=viajes_staff)

    def perform_create(self, serializer):

        if not self.request.user.is_superuser:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Solo el administrador puede crear envíos.")

        serializer.save()

    def perform_update(self, serializer):

        if not self.request.user.is_superuser:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("No tienes permiso para modificar este envío.")

        serializer.save()

    def perform_destroy(self, instance):

        if not self.request.user.is_superuser:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied("Solo el administrador puede eliminar envíos.")

        instance.delete()


# ============================================================
# ME
# ============================================================
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Superusuario
        if user.is_superuser:
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "tipo": "superuser",
                }
            )

        # Usuario que tiene relación con Cliente
        if hasattr(user, "cliente"):
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "tipo": "cliente",
                    "cliente_id": user.cliente.id,
                }
            )

        # Usuario que pertenece a Staff
        staff = StaffViaje.objects.filter(usuario=user).select_related("viaje")

        if staff.exists():
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "tipo": "staff",
                    "viajes": [
                        {
                            "id": miembro.viaje.id,
                            "nombre": miembro.viaje.nombre,
                            "rol": miembro.rol,
                        }
                        for miembro in staff
                    ],
                }
            )

        # Usuario autenticado pero sin relación definida
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "tipo": "usuario",
            }
        )
