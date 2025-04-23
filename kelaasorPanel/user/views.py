from kavenegar import *
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
import random
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from .tasks import get_verification_code
import json
from rest_framework import status
from rest_framework.response import Response
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, AllowAny

api = KavenegarAPI('2F3441543830615A2B71616F7831315162635563767459776A435A70783348794D39393175506545596D6B3D')  # بهتره اینو در settings بذاری


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class GetVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        phone_number = data.get("phone_number")

        if not phone_number:
            return Response({"status": "error", "message": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        code = random.randint(100000, 999999)
        get_verification_code.delay(code, phone_number)

        return Response({"status": "success", "message": "Verification code sent."}, status=status.HTTP_200_OK)
    

class VerifyCodeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            input_code = data.get("verification_code")
        except (json.JSONDecodeError, TypeError):
            return Response({"status": "error", "message": "Invalid JSON."}, status=status.HTTP_400_BAD_REQUEST)

        cached_code = cache.get('validate_code')
        print("Incoming code:", input_code)
        print("Cached code:", cached_code)

        if not cached_code:
            return Response({"status": "error", "message": "Code expired or not found."}, status=status.HTTP_400_BAD_REQUEST)

        if str(input_code).strip() == str(cached_code).strip():
            return Response({"status": "success", "message": "Code is correct."}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)