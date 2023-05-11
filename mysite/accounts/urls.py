from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    # login 
    path('login/', views.LoginView.as_view(), name='login'),
    # logout
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # signup
    path('signup/', views.SignupView.as_view(), name='signup'),
    # api
    path('api/v1/', include('accounts.api.v1.urls'))
]