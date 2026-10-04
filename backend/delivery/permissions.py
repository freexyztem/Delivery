from rest_framework.permissions import BasePermission

from .models import StaffViaje


class EsAdministrador(BasePermission):
    """
    Solo el superusuario puede administrar todo.
    """

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_superuser
        )


class EsStaff(BasePermission):
    """
    Comprueba que el usuario pertenece al viaje específico.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        viaje = getattr(obj, "viaje", None)

        if viaje is None:
            return False

        return StaffViaje.objects.filter(
            viaje=viaje,
            usuario=request.user,
        ).exists()


class EsRepartidorDelViaje(BasePermission):
    """
    Comprueba que el usuario es REPARTIDOR
    del viaje específico.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        viaje = getattr(obj, "viaje", None)

        if viaje is None:
            return False

        return StaffViaje.objects.filter(
            viaje=viaje,
            usuario=request.user,
            rol=StaffViaje.Rol.REPARTIDOR,
        ).exists()


class EsCliente(BasePermission):
    """
    Comprueba que el usuario sea un cliente.

    En el nuevo modelo no existe Cliente.
    Todo usuario que no sea staff ni superusuario
    se considera cliente.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and not request.user.is_staff
            and not request.user.is_superuser
            and request.user.is_active
        )

    def has_object_permission(self, request, view, obj):

        if not self.has_permission(request, view):
            return False

        return obj.producto.cliente_id == request.user.id


class EsPropietarioDelEnvio(BasePermission):
    """
    Comprueba que el envío pertenece
    al cliente autenticado.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        return (
            not request.user.is_staff
            and request.user.is_active
            and obj.producto.cliente_id == request.user.id
        )
