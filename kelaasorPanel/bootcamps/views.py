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
    queryset = BootCampsJoinRequest.objects.all()
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampsJoinRequestSerializer
    
    
class ListBootcampsJoinRequestsView(ListAPIView):
    queryset = BootCampsJoinRequest.objects.filter(state="pending")
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampsJoinRequestSerializer


class DecideBootcampJoinRequestState(UpdateAPIView):
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
    queryset = BootCampsJoinRequest.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BootCampsJoinRequestSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateBootcampCategoryView(CreateAPIView):
    queryset = BootCampCategory.objects.all()
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampCategorySerializer


class CreateBootcampView(CreateAPIView):
    queryset = BootCamp.objects.all()
    permission_classes = [IsSuperUserType]
    serializer_class = BootCampSerializer


class ListBootCampCategory(ListAPIView):
    queryset = BootCampCategory.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BootCampCategorySerializer
    

class ListBootcampsView(ListAPIView):
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

