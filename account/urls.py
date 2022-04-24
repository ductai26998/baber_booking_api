from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from service import views as service_views

router = DefaultRouter()

router.register("user", views.UserViewSet)
router.register("salon", views.SalonViewSet)
# router.register("address", views.AddressViewSet)
router.register("salon-service", service_views.ServiceSalonViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("salon-update-address", views.AddressUpdate.as_view()),
]
