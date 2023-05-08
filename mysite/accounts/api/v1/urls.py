from django.urls import path
from . import views

app_name = 'api-v1'

urlpatterns = [
    # registration
    path('register/', views.UserRegisterApiView.as_view(), name='register')

    # change password
    # reset password
    # login token
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),
    # login jwt
]