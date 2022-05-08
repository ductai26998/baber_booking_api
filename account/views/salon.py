from .address import Address
from base.views import BaseViewSet
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms.utils import ErrorDict

from . import AccountErrorCode, models
from ..serializers import (
    AddressSerializer,
    SalonRegisterInputSerializer,
    SalonRegisterSerializer,
    SalonSerializer,
)


class SalonViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = models.Salon.objects.filter()
    serializer_class = SalonSerializer
    permission_map = {
        "destroy": [IsAdminUser],
    }

    def list(self, request):
        search_query = request.query_params.get("q", "")
        sort_query = request.query_params.get("sort", "")
        queryset = models.Salon.objects.filter(salon_name__icontains=search_query)

        if sort_query:
            try:
                if sort_query.startswith("-"):
                    models.Salon._meta.get_field(sort_query[1:])
                else:
                    models.Salon._meta.get_field(sort_query)
                queryset = queryset.order_by(sort_query)

            except:
                pass
        self.queryset = queryset
        return super().list(request)

    def create(self, request):
        response = {
            "code": AccountErrorCode.NOT_FOUND,
            "detail": "Create function is not offered in this path.",
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        if str(request.user.id) != pk:
            return Response(
                {
                    "code": AccountErrorCode.PERMISSION_DENIED,
                    "detail": "Permission denied",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().partial_update(
            request,
            pk,
            code=AccountErrorCode.INVALID,
            fail_detail="Update salon info was failed",
            success_detail="Update the salon info successful",
        )

    def destroy(self, request, pk=None):
        try:
            salon = models.Salon.objects.get(pk=pk)
            if not salon:
                return Response(
                    {
                        "code": AccountErrorCode.INACTIVE,
                        "detail": "Salon is inactive",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            salon.is_active = False
            salon.save()
            return Response(
                {
                    "detail": "Salon is deactivated",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "detail": "Deactivation failed",
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


class SalonRegister(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            address_url = data.get("address_url")
            if not address_url or address_url.strip() == "":
                return Response(
                    {
                        "code": AccountErrorCode.REQUIRED,
                        "detail": "Address url is required",
                        "messages": {"address_url": ["Address url is required"]},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serialize_account = SalonRegisterInputSerializer(data=data)
            if serialize_account.is_valid():
                serialize_account.validated_data
                serialize_account.save()
                email = serialize_account.data["email"]
                account = models.Salon.objects.get(email=email)
                account.is_salon = True
                account.is_active = True

                # create address
                address = Address()
                address.set_address_from_url(address_url)
                account_address = models.Address.objects.create(
                    address=address.address,
                    province=address.province,
                    district=address.district,
                    ward=address.ward,
                    hamlet=address.hamlet,
                    lat=address.lat,
                    lng=address.lng,
                    position_url=address.position_url,
                )

                account.address = account_address
                account.save()
                token = RefreshToken.for_user(account)
                response = SalonRegisterSerializer(account)

                return Response(
                    {
                        "detail": "Registration successfully, check email to get otp",
                        "data": {
                            **response.data,
                            "access_token": str(token.access_token),
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "detail": "Register salon failed",
                    "messages": serialize_account.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "detail": "Register salon failed",
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class AddressUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def put(self, request):
        try:
            account = request.user
            data = request.data
            address_url = data.get("address_url")
            if address_url.strip() == "":
                return Response(
                    {
                        "code": AccountErrorCode.REQUIRED,
                        "detail": "Address url is required",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            address = Address()
            address.set_address_from_url(address_url)
            current_address = account.address

            current_address.address = address.address
            current_address.province = address.province
            current_address.district = address.district
            current_address.ward = address.ward
            current_address.hamlet = address.hamlet
            current_address.lat = float(
                address.lat,
            )
            current_address.lng = float(
                address.lng,
            )
            current_address.position_url = address.position_url
            current_address.save()

            serializer = AddressSerializer(current_address)
            return Response(
                {
                    "detail": "Update address successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "detail": "Update address failed",
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


# class AddressViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = models.Address.objects.all()
#     serializer_class = AddressSerializer


# class GetServicesOfSalon(APIView):
#     def get(self, request):
#         try:
#             salon_id = request.data.get("salon_id")
#             services = service_models.ServiceSalon.objects.filter(salon_id=salon_id)
#             # queryset = self.filter_queryset(self.get_queryset())

#             # page = self.paginate_queryset(queryset)
#             # if page is not None:
#             #     serializer = self.get_serializer(page, many=True)
#             #     return self.get_paginated_response(serializer.data)

#             # serializer = self.get_serializer(queryset, many=True)
#             # return Response(serializer.data)
#             print(services)
#             return Response(
#                 {
#                     "message": "Get services of salon successfully",
#                     "data": services,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except Exception as e:
#             return Response(
#                 {
#                     "code": AccountErrorCode.PROCESSING_ERROR,
#                     "message": "Can not get the services of salon",
#                     "errors": e.args,
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#                 exception=e,
#             )
