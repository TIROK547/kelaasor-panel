from kavenegar import KavenegarAPI
from .models import User
from .serializers import UserSerializer, CustomAccountSerializer, CreateAccountSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
import random
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import Group
from .tasks import get_verification_code
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

api = KavenegarAPI('2F3441543830615A2B71616F7831315162635563767459776A435A70783348794D39393175506545596D6B3D')
# TODO: Move API key to Django settings for security


"""code complete kossher :)"""
# class CreateUserView(CreateAPIView):
#     """
#     API view to create a new user and assign a default group.
#     """
#     permission_classes = [AllowAny]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

#     @staticmethod
#     def assign_group(user, role_name="default user"):
#         """
#         Assign the specified group to the user if it exists.
#         """
#         try:
#             group = Group.objects.get(name=role_name)
#             user.groups.add(group)
#             user.save()
#         except Group.DoesNotExist:
#             pass

#     def perform_create(self, serializer):
#         """
#         Save the new user and assign the default group.
#         """
#         user = serializer.save()
#         self.assign_group(user)


class RegisterAccountView(APIView):
    """امکان ساختن اکانت برای کاربر و دریافت توکن بعد از ساختن همچنین برای جلوگیری از ذخیره اطلاعات ناقص از رول بک استفاده شده"""
    permission_classes = [AllowAny]
    def post(self, request):
        with transaction.atomic():
            serializer = CreateAccountSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                refresh = RefreshToken.for_user(user)

                return Response({
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                    },status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#test passed
#ویرایش اکانت برای کاربر عادی
class EditAccountView(UpdateAPIView):
    """ کاربر میتونه اکانت خودشو ادیت کنه اگه اهراز هویت شده باشه """
    permission_classes = [IsAuthenticated]
    serializer_class = CreateAccountSerializer

    def get_object(self):
        return self.request.user
    


#برای خروج کاربر
class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "User Logged Out Successfully!"})
        except Exception:
            return Response({"detail": "Error during logout, please try again later."}, status=500)



    


#test passed
class DetailAccountView(RetrieveAPIView):
    """ کاربر میتونه اکانت خودشو ببینه  کنه اگه اهراز هویت شده باشه """
    permission_classes = [IsAuthenticated]
    serializer_class = CustomAccountSerializer


    def get_object(self):
        return self.request.user





class GetVerificationCodeView(APIView):
    """
    API endpoint to generate and send a verification code via SMS.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Accepts a phone number and triggers sending a verification code asynchronously.
        """
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response(
                {"status": "error", "message": "Phone number is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        code = random.randint(100000, 999999)
        get_verification_code.delay(code, phone_number)
        return Response(
            {"status": "success", "message": "Verification code sent."},
            status=status.HTTP_200_OK
        )


class VerifyCodeView(APIView):
    """
    API endpoint to verify the submitted verification code.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Validates the verification code provided by the user against the cached code.
        """
        input_code = request.data.get("verification_code")
        if input_code is None:
            return Response(
                {"status": "error", "message": "Verification code is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cached_code = cache.get('validate_code')

        if not cached_code:
            return Response(
                {"status": "error", "message": "Code expired or not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if str(input_code).strip() == str(cached_code).strip():
            return Response(
                {"status": "success", "message": "Code is correct."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"status": "error", "message": "Invalid verification code."},
                status=status.HTTP_400_BAD_REQUEST
            )
