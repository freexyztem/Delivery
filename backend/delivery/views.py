from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .models import (
    StaffViaje,
    Tarifa,
    Viaje,
    Producto,
    Envio,
)

from .permissions import (
    EsAdministrador,
    EsStaff,
    EsRepartidorDelViaje,
    EsCliente,
    EsPropietarioDelEnvio,
)

from .serializers import (
    StaffSerializer,
    UserSerializer,
    TarifaSerializer,
    ViajeSerializer,
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

    # Solo el administrador puede acceder a /usuarios/
    permission_classes = [EsAdministrador]


# ============================================================
# TARIFAS
# ============================================================


class TarifaViewSet(viewsets.ModelViewSet):

    queryset = Tarifa.objects.all()

    serializer_class = TarifaSerializer

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

    queryset = StaffViaje.objects.select_related(
        "viaje",
        "usuario",
    ).all()

    serializer_class = StaffSerializer

    permission_classes = [IsAuthenticated]


# ============================================================
# PRODUCTOS
# ============================================================


class ProductoViewSet(viewsets.ModelViewSet):

    queryset = Producto.objects.select_related(
        "cliente",
    ).all()

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
    ).all()

    serializer_class = EnvioSerializer

    def get_permissions(self):

        # ADMINISTRADOR
        if self.request.user.is_superuser:
            return [EsAdministrador()]

        # STAFF
        if self.request.user.is_staff:
            return [EsStaff()]

        # CLIENTE
        return [EsCliente()]

    def get_queryset(self):

        user = self.request.user

        # SUPERUSUARIO
        if user.is_superuser:
            return self.queryset

        # CLIENTE
        if not user.is_staff:
            return self.queryset.filter(producto__cliente=user)

        # STAFF
        viajes_staff = StaffViaje.objects.filter(usuario=user).values_list(
            "viaje_id",
            flat=True,
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

        # ====================================================
        # SUPERUSUARIO
        # ====================================================

        if user.is_superuser:

            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "tipo": "superuser",
                }
            )

        # ====================================================
        # STAFF
        # ====================================================

        if user.is_staff:

            staff = StaffViaje.objects.filter(usuario=user).select_related("viaje")

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

        # ====================================================
        # CLIENTE
        # ====================================================

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "tipo": "cliente",
            }
        )


# ============================================================
# USUARIO ACTUAL
# ============================================================


class UsuarioActualView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        usuario = request.user

        if usuario.is_superuser:

            rol = "admin"

        elif usuario.is_staff:

            rol = "staff"

        else:

            rol = "cliente"

        return Response(
            {
                "id": usuario.id,
                "username": usuario.username,
                "rol": rol,
            }
        )
