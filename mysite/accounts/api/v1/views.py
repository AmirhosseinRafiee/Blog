from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.views import TokenObtainPairView
from ...models import Profile
from .serializers import RegistrationSerializer, ChangePasswordSerializer, ProfileSerializer, CustomAuthTokenSerializer, CustomTokenObtainPairSerializer
from .permissions import IsNotAuthenticated

class UserRegisterApiView(GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsNotAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.validated_data['email'],
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordApiView(GenericAPIView):
  serializer_class = ChangePasswordSerializer
  permission_classes = [IsAuthenticated]

  def put(self, request, *args, **kwargs):
    user = request.user
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not user.check_password(serializer.validated_data['old_password']):
      return Response({'old password': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(serializer.validated_data['new_password'])
    user.save()
    return Response({'detail': 'password changed successfully'}, status=status.HTTP_200_OK)

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
    user = serializer.validated_data['user']
    token, created = Token.objects.get_or_create(user=user)
    return Response({
      'token': token.key,
      'user_id': user.pk,
      'email': user.email,
    })

class CustomDiscardAuthToken(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request, *args, **kwargs):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
class CustomTokenObtainPairView(TokenObtainPairView):
  serializer_class = CustomTokenObtainPairSerializer


class TestSendEmail(APIView):

  def get(self, request, *args, **kwargs):
    send_mail(
      subject = "Test Email",
      message = "This is a test email",
      from_email = None,   # This will have no effect is you have set DEFAULT_FROM_EMAIL in settings.py
      recipient_list = ['your_recipient_email'],    # This is a list
      fail_silently = False   
    )
    return Response('email sent')