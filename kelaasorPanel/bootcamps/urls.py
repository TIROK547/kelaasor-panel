from django.urls import path
from .views import ListBootCampCategory, ListBootcampsView

urlpatterns = [
    path("categories/", ListBootCampCategory.as_view()),
    path("", ListBootcampsView.as_view()),
]