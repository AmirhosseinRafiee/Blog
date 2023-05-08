from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer, CustomAuthTokenSerializer
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