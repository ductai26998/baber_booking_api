from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('user', views.UserViewSet)
router.register('salon', views.SalonViewSet)
router.register('address', views.AddressViewSet)
# router.register(r'address/create', views.AddressCreate.as_view(), basename = "address-create")

urlpatterns = [
    path('', include(router.urls)),
    path('address/create', views.AddressCreate.as_view())
]
