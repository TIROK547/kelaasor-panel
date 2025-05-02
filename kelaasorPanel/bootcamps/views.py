from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from .serializers import BootCampSerializer, BootCampCategorySerializer
from .models import BootCampCategory, BootCamp
from rest_framework.permissions import AllowAny, IsAuthenticated

#test
class ListBootCampCategory(ListAPIView):
    queryset = BootCampCategory.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BootCampCategorySerializer
    
    
class ListBootcampsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = BootCampSerializer
    
    def get_queryset(self, request):
        data = request.data
        state = data.get("state", None)
        category_id = data.get("category_id", None)
        
        filters = {}
        if category_id:
            filters["category_id"] = category_id
        if state:
            filters["bootcamp_state"] = state

        bootcamps = BootCamp.objects.filter(**filters)
        return bootcamps
    
