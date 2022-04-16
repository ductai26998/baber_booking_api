from rest_framework import viewsets
from rest_framework import views
from rest_framework.response import Response
from core import ResponseStatusCode
from django.core.exceptions import ValidationError


class BaseViewSet(viewsets.ModelViewSet):
    serializer_class = None
    required_alternate_scopes = {}
    serializer_map = {}
    permission_map = {}

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_permissions(self):
        return [permission() for permission in self.permission_map.get(self.action, self.permission_classes)]


class BaseAPIView(views.APIView):
    @classmethod
    def get_instance(self, request, **kwargs):
        instance = request.user
        if instance.is_anonymous:
            raise ValidationError("Permission denied", code="Error")
            # raise ValidationError({"sss_id": ValidationError(
            #     "This user have orders", code="INVALID")})
            # return Response({
            #     "status": ResponseStatusCode.ERROR,
            #     "message": "Permission denied",
            # })
        return instance

    @classmethod
    def post(self, request, **kwargs):
        self.get_instance(request, **kwargs)
