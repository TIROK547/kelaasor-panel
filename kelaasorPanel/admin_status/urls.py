from django.urls import path
from .views import ChangeUserGroupView

urlpatterns = [
    path("change-staff/<int:user_id>", ChangeUserGroupView.as_view())
]