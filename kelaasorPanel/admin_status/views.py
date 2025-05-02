from django.shortcuts import render
from user.models import User
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUserType
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from django.contrib.auth.models import Group

class ChangeUserGroupView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUserType]

    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404("User not found")

        # Check if the user is authorized to make the change
        if not request.user.is_superuser:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        # Get the 'make_admin' field from the request body, defaulting to False
        make_admin = request.data.get('make_admin', None)
        admin_type = request.data.get("admin_type", None)
        
        if make_admin is None:
            return Response({"detail": "The 'make_admin' field is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(make_admin, bool):
            return Response({"detail": "'make_admin' must be a boolean value."}, status=status.HTTP_400_BAD_REQUEST)

        # Toggle the user's admin status (is_staff or is_superuser)
        if make_admin:
            user.is_staff = True  # Set as admin
            if admin_type:
                try:
                    group = Group.objects.get(name=admin_type)  # Get the group by name
                    user.groups.clear()  # Clear any existing groups
                    user.groups.add(group)  # Add the new group
                except Group.DoesNotExist:
                    return Response({"detail": f"Group '{admin_type}' not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.is_staff = False  # Revoke admin privileges
            user.groups.clear()  # Remove all groups
            
        user.save()

        return Response({
            "detail": "User role updated successfully.",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
