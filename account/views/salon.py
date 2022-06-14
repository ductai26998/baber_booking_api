from base.services.cloudinary import CloudinaryService
from base.views import BaseViewSet
from booking.serializers import BookingSerializer
from django.conf import settings
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from service.serializers import ServiceSalonSerializer

from ..serializers import (
    AddressSerializer,
    AddressSerializerInput,
    SalonRegisterInputSerializer,
    SalonRegisterSerializer,
    SalonSerializer,
)
from . import AccountErrorCode, models
from .address import Address


class SalonViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    queryset = models.Salon.objects.filter()
    serializer_class = SalonSerializer
    permission_map = {
        "destroy": [IsAdminUser],
    }

    @action(detail=True)
    def services(self, request, *args, **kwargs):
        """
        Returns a list of all the group names that the given
        user belongs to.
        """
        user = self.get_object()
        services = user.services.all()
        data = [ServiceSalonSerializer(service).data for service in services]
        response_dict = {
            "detail": None,
            "data": data,
            "error": None,
        }
        return Response(response_dict)

    @action(detail=True)
    def bookings(self, request, *args, **kwargs):
        """
        Returns a list of all the bookings that the given
        user belongs to.
        """
        requester_id = request.user.id
        salon = models.Salon.objects.filter(id=requester_id).first()
        if not salon:
            return Response(
                {
                    "code": AccountErrorCode.NOT_FOUND,
                    "detail": "Salon %s is not exist" % requester_id,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        search_query = request.query_params.get("status", "")
        bookings = salon.bookings.all()
        if search_query:
            bookings = bookings.filter(status=search_query)
        data = [BookingSerializer(booking).data for booking in bookings]
        response_dict = {
            "detail": None,
            "data": data,
            "error": None,
        }
        return Response(response_dict)

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

        avatar = request.FILES.get("avatar")
        avatar_folder_path = settings.CLOUDINARY_AVATAR_USER_FOLDER + pk + "/"
        url = CloudinaryService.upload_image(avatar, avatar_folder_path)
        request.data["avatar"] = url
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
            serializer_salon = SalonRegisterInputSerializer(data=data)
            if serializer_salon.is_valid():
                serializer_salon.validated_data
                serializer_salon.save()
                email = serializer_salon.data["email"]
                salon = models.Salon.objects.get(email=email)
                salon.is_salon = True
                salon.save(update_fields=("is_salon",))

                if data.get("address") and data.get("address").get("position_url"):
                    address_ref = Address()
                    lat, lng = address_ref.get_position_from_url(
                        data.get("address").get("position_url")
                    )
                    address = salon.address
                    address.lat = lat
                    address.lng = lng

                token = RefreshToken.for_user(salon)
                response = SalonRegisterSerializer(salon)

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
                    "messages": serializer_salon.errors,
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
            address = request.user.address
            serializer = AddressSerializerInput(data=request.data)
            if serializer.is_valid():
                data = serializer.data
                for key in data:
                    value = data[key]
                    if value and value.strip() != "":
                        setattr(address, key, value)

                address_ref = Address()
                position_url = data.get("position_url")
                lat, lng = address_ref.get_position_from_url(position_url)
                address.lat = lat
                address.lng = lng
                address.save()
                response = AddressSerializer(address)
                return Response(
                    {
                        "detail": "Update address successfully",
                        "data": response.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "detail": "Register salon failed",
                    "messages": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {
                    "code": AccountErrorCode.PROCESSING_ERROR,
                    "detail": "Update address failed",
                    "messages": e.args,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
