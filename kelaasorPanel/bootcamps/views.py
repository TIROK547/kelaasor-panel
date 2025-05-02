from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from .serializers import BootCampSerializer, BootCampCategorySerializer
from .models import BootCampCategory, BootCamp, BootCampsJoinRequest
from rest_framework.permissions import AllowAny, IsAuthenticated


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

