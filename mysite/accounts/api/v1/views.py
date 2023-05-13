from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.conf import settings
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from mail_templated import EmailMessage
from ...models import Profile
from .serializers import (
    RegistrationSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ActivationResendSerializer,
)
from .permissions import IsNotAuthenticated
from .utils import EmailTread

User = get_user_model()


class UserRegisterApiView(GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user = User.objects.get(email=email)
            token = self.get_access_token_for_user(user)
            email_obj = EmailMessage(
                "email/activation.tpl",
                {"token": token},
                "admin@admin.com",
                to=[user.email],
            )
            EmailTread(email_obj).start()
            data = {
                "email": serializer.validated_data["email"],
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_access_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(minutes=10))
        return str(access_token)


class ChangePasswordApiView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"old password": "wrong password"}, status=status.HTTP_400_BAD_REQUEST
            )
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(
            {"detail": "password changed successfully"}, status=status.HTTP_200_OK
        )


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()

    def get_object(self):
        profiles = self.get_queryset()
        profile = get_object_or_404(profiles, user=self.request.user)
        return profile


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
            }
        )


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            decode_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decode_jwt["user_id"]
        except jwt.exceptions.ExpiredSignatureError:
            return Response(
                {"detail": "token has been expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.InvalidSignatureError:
            return Response(
                {"detail": "token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.PyJWTError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=user_id)
        if user.is_verified:
            return Response(
                {"detail": "your account has already been verified"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user.is_verified = True
        user.save()
        return Response(
            {"detail": "your account have been verified successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ActivationResendApiView(GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = self.get_access_token_for_user(user)
        email_obj = EmailMessage(
            "email/activation.tpl", {"token": token}, "admin@admin.com", to=[user.email]
        )
        EmailTread(email_obj).start()
        return Response(
            {"detail": "user activation resend successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def get_access_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(minutes=10))
        return str(access_token)


class TestSendEmail(APIView):
    def get(self, request, *args, **kwargs):
        email = "test@test.com"
        user = get_object_or_404(User, email=email)
        token = self.get_access_token_for_user(user)
        email_obj = EmailMessage(
            "email/hello.tpl", {"token": token}, "admin@admin.com", to=[user.email]
        )
        EmailTread(email_obj=email_obj).start()
        return Response("email sent")

    def get_access_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        # access_token = refresh.access_token
        # access_token.set_exp(lifetime=timedelta(minutes=10))
        return str(refresh.access_token)
