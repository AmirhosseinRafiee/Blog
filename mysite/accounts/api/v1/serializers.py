from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({'detail': 'Password does not match'})
        try:
            validate_password(password)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('password2', None)
        return User.objects.create_user(**validated_data)

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validate_data =  super().validate(attrs)
        validate_data['email'] = self.user.email
        validate_data['user_id'] = self.user.id
        return validate_data