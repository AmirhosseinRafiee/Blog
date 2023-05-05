from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import Response, APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ...models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import PostFilter, PostCustomOrderFilter
from .paginations import CustomPagination

# fbv
# @api_view()
# @permission_classes([IsAuthenticated])
# def post_list(request):
#     posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
#     if not request.user.is_authenticated:
#         posts = posts.filter(login_require=False)
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def create_post(request):
#     serializer = PostSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save()
#     return Response(serializer.data)

# ApiViews
# class PostListApiView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
#         if not request.user.is_authenticated:
#             posts = posts.filter(login_require=False)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
# class PostDetailApiView(APIView):
#     permission_classes = [IsOwnerOrReadOnly]

#     def get(self, request, id):
#         posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
#         if not request.user.is_authenticated:
#             posts = posts.filter(login_require=False)
#         post = get_object_or_404(posts, pk=id)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
#         if not request.user.is_authenticated:
#             posts = posts.filter(login_require=False)
#         post = get_object_or_404(posts, pk=id)
#         serializer = PostSerializer(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
#     def delete(self, request, id):
#         posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
#         if not request.user.is_authenticated:
#             posts = posts.filter(login_require=False)
#         post = get_object_or_404(posts, pk=id)
#         post.delete()
#         return Response({'detail': 'item removed successfully'}, status=status.HTTP_204_NO_CONTENT)

# class PostListApiView(ListCreateAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
#         if not self.request.user.is_authenticated:
#             posts = posts.filter(login_require=False)
#         return posts
    
# class PostDetailApiView(RetrieveUpdateDestroyAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
#         if not self.request.user.is_authenticated:
#             posts = posts.filter(login_require=False)
#         return posts
    
# class PostViewSet(ViewSet):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     queryset = Post.objects.filter(status=True)
#     serializer_class = PostSerializer

class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly ,IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, PostCustomOrderFilter]
    filterset_class = PostFilter
    search_fields = ['author__last_name', 'title', 'content']
    ordering_fields = ['published_date', 'counted_view']
    # ordering = ['-published_date']

    def get_queryset(self):
        posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
        if not self.request.user.is_authenticated:
            posts = posts.filter(login_require=False)
        return posts


