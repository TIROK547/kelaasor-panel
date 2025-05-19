from django.shortcuts import get_object_or_404
from user.models import User
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUserType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Group

class ChangeUserGroupView(APIView):
    """
    Allows superusers to assign or revoke admin status and set user groups.
    """
    permission_classes = [IsAuthenticated, IsSuperUserType]

    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)

        make_admin = request.data.get('make_admin')
        admin_type = request.data.get('admin_type')

        if make_admin is None:
            return Response({"detail": "The 'make_admin' field is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(make_admin, bool):
            return Response({"detail": "'make_admin' must be a boolean value."}, status=status.HTTP_400_BAD_REQUEST)

        if make_admin:
            user.is_staff = True
            if admin_type:
                try:
                    group = Group.objects.get(name=admin_type)
                    user.groups.clear()
                    user.groups.add(group)
                except Group.DoesNotExist:
                    return Response({"detail": f"Group '{admin_type}' not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_staff = False
            user.groups.clear()

        user.save()

        return Response({
            "detail": "User role updated successfully.",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
