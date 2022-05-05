from django.core.exceptions import ValidationError
from rest_framework import status, views, viewsets
from rest_framework.response import Response


class BaseViewSet(viewsets.ModelViewSet):
    serializer_class = None
    required_alternate_scopes = {}
    serializer_map = {}
    permission_map = {}

    def get_serializer_class(self):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_map.get(
                self.action, self.permission_classes
            )
        ]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print(response.data)
        if response.status_code < 400:
            return Response(
                {
                    "data": response.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": response.text,
                    "errors": response.data,
                },
                status=response.status_code,
            )

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        print(response.data)
        if response.status_code < 400:
            return Response(
                {
                    "data": response.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "message": response.text,
                    "errors": response.json(),
                },
                status=response.status_code,
            )


class BaseAPIView(views.APIView):
    @classmethod
    def get_instance(self, request, **kwargs):
        instance = request.user
        if instance.is_anonymous:
            raise ValidationError("Permission denied", code="Error")
        return instance

    @classmethod
    def post(self, request, **kwargs):
        self.get_instance(request, **kwargs)
