from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from .serializers import BootCampSerializer, BootCampCategorySerializer, BootCampsJoinRequestSerializer
from .models import BootCampCategory, BootCamp, BootCampsJoinRequest
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from admin_status.permissions import IsSuperUserType
from django.db.models import Q
from financial.models import Factor
from rest_framework.response import Response
from rest_framework import status as drf_status


class ListAllBootcampsJoinRequestsView(ListAPIView):
    """
    Lists all bootcamp join requests.
    Accessible only to superusers.
    """
    queryset = BootCampsJoinRequest.objects.all()
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampsJoinRequestSerializer
    
    
class ListBootcampsJoinRequestsView(ListAPIView):
    """
    Lists only pending bootcamp join requests.
    Accessible only to superusers.
    """
    queryset = BootCampsJoinRequest.objects.filter(state="pending")
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampsJoinRequestSerializer


class DecideBootcampJoinRequestState(UpdateAPIView):
    """
    Updates the state of a join request. If the new state is 'accepted' and no related Factor exists,
    a Factor is automatically created.
    """
    queryset = BootCampsJoinRequest.objects.all()
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampsJoinRequestSerializer
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        prev_state = instance.state

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        new_state = instance.state

        if new_state == 'accepted' and prev_state != 'accepted':
            if not Factor.objects.filter(request=instance).exists():
                Factor.objects.create(
                    bootcamp=instance.bootCamp,
                    user=instance.user,
                    request=instance
                )

        return Response(serializer.data, status=drf_status.HTTP_200_OK)
    

class CreateBootcampJoinRequestView(CreateAPIView):
    """
    Allows an authenticated user to submit a join request to a bootcamp.
    """
    queryset = BootCampsJoinRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BootCampsJoinRequestSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateBootcampCategoryView(CreateAPIView):
    """
    Allows a superuser to create a new bootcamp category.
    """
    queryset = BootCampCategory.objects.all()
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampCategorySerializer


class CreateBootcampView(CreateAPIView):
    """
    Allows a superuser to create a new bootcamp.
    """
    queryset = BootCamp.objects.all()
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampSerializer


class ListBootCampCategory(ListAPIView):
    """
    Public view to list all bootcamp categories.
    """
    queryset = BootCampCategory.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BootCampCategorySerializer
    

class ListBootcampsView(ListAPIView):
    """
    Public view to list all bootcamps, with optional filtering by state and category_id.
    """
    permission_classes = [AllowAny]
    serializer_class = BootCampSerializer

    def get_queryset(self):
        state = self.request.query_params.get("state")
        category_id = self.request.query_params.get("category_id")

        filters = {}
        if category_id:
            filters["category_id"] = category_id
        if state:
            filters["bootcamp_state"] = state
            
        return BootCamp.objects.filter(**filters)
