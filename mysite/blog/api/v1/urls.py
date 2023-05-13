# from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register("posts", views.PostViewSet, basename="post")
urlpatterns = router.urls

# urlpatterns = [
# path('', views.post_list, name='post-list'),
# path('create/', views.create_post, name='post-create'),
# path('', views.PostListApiView.as_view(), name='post-list'),
# path('post/<int:id>/', views.PostDetailApiView.as_view(), name='post-detail'),
#     path('', views.PostListApiView.as_view(), name='post-list'),
#     path('post/<int:pk>/', views.PostDetailApiView.as_view(), name='post-detail'),
# ]
