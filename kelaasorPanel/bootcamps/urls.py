from django.urls import path
from .views import (
    ListBootCampCategory, ListBootcampsView, CreateBootcampJoinRequestView
    )

urlpatterns = [
    path("categories/", ListBootCampCategory.as_view()),
    path("", ListBootcampsView.as_view()),
    path("join/", CreateBootcampJoinRequestView.as_view())
]