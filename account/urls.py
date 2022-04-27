from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import salon as salon_views
from .views import user as user_views
from service import views as service_views

router = DefaultRouter()

router.register("user", user_views.UserViewSet)
router.register("salon", salon_views.SalonViewSet)

router.register("salonService", service_views.ServiceSalonViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # apis for salon
    path("salonAddress/", salon_views.AddressUpdate.as_view()),
    # apis for user
]
