from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('user', views.UserViewSet)
router.register('salon', views.SalonViewSet)
router.register('address', views.AddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('address/create', views.AddressCreate.as_view())
]
