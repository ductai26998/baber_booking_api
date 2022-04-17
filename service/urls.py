from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('', views.ServiceViewSet)
# router.register('salon-service', views.ServiceSalonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
