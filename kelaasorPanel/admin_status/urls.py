from django.urls import path
from .views import ChangeUserGroupView
from bootcamps.views import CreateBootcampView, CreateBootcampCategoryView, DecideBootcampJoinRequestState, ListBootcampsJoinRequestsView, ListAllBootcampsJoinRequestsView

urlpatterns = [
    path("change-staff/<int:user_id>", ChangeUserGroupView.as_view()),
    path("create-bootcamp/", CreateBootcampView.as_view()),
    path("create-bootcamp/category/", CreateBootcampCategoryView.as_view()),
    path("bootcamp/join-requests/decide/<int:pk>/", DecideBootcampJoinRequestState.as_view()),
    path("bootcamp/join-requests/pending", ListBootcampsJoinRequestsView.as_view()),
    path("bootcamp/join-requests/all", ListAllBootcampsJoinRequestsView.as_view()),
]