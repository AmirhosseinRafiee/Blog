from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .. import views

urlpatterns = [
    # registration
    path('register/', views.UserRegisterApiView.as_view(), name='register'),

    path('test-email/', views.TestSendEmail.as_view(), name='test-email'),
    # change password
    path('change-password/', views.ChangePasswordApiView.as_view(), name='change-password'),
    # reset password
    # login token
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),
    # login jwt
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]