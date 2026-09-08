from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    TarifaViewSet,
    ClienteViewSet,
    ViajeViewSet,
    StaffViewSet,
    ProductoViewSet,
    EnvioViewSet,
    MeView,
)

router = DefaultRouter()


router.register("usuarios", UserViewSet, basename="usuarios")

router.register("tarifas", TarifaViewSet, basename="tarifas")

router.register("clientes", ClienteViewSet, basename="clientes")

router.register("viajes", ViajeViewSet, basename="viajes")

router.register("staff", StaffViewSet, basename="staff")

router.register("productos", ProductoViewSet, basename="productos")

router.register("envios", EnvioViewSet, basename="envios")


urlpatterns = [
    path("", include(router.urls)),
    path("me/", MeView.as_view(), name="me"),
]
