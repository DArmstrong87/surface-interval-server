from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from surfaceintervalapi.views import (
    register_user,
    login_user,
    DiveView,
    DiverView,
    SpecialtyView,
    CustomGearTypeView,
    CertCardView,
    GearSetView,
    GearItemView,
    GearItemServiceView,
    GearItemVServiceIntervalView,
    GearTypeView,
    ImageView,
    HealthCheckView,
)


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"cert-cards", CertCardView, "cert-card")
router.register(r"custom-gear-types", CustomGearTypeView, "specialty")
router.register(r"dives", DiveView, "dive")
router.register(r"divers", DiverView, "diver")
router.register(r"gear-items", GearItemView, "gear-item")
router.register(r"gear-item-services", GearItemServiceView, "gear-item-service")
router.register(
    r"gear-item-service-intervals", GearItemVServiceIntervalView, "gear-item-service-interval"
)
router.register(r"gear-sets", GearSetView, "gear-set")
router.register(r"gear-types", GearTypeView, "gear-type")
router.register(r"images", ImageView, "image")
router.register(r"specialties", SpecialtyView, "specialty")


urlpatterns = [
    path("", include(router.urls)),
    path("register", register_user),
    path("login", login_user, name="login"),
    path("healthcheck", HealthCheckView.as_view(), name="healthcheck"),
    # Generate raw OpenAPI schema (YAML or JSON)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Interactive Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api-auth", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]
