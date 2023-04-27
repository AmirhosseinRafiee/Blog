from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import Response, APIView
from rest_framework import status
from ...models import Post
from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

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

class PostListApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
        if not request.user.is_authenticated:
            posts = posts.filter(login_require=False)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class PostDetailApiView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, id):
        posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
        if not request.user.is_authenticated:
            posts = posts.filter(login_require=False)
        post = get_object_or_404(posts, pk=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, id):
        posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
        if not request.user.is_authenticated:
            posts = posts.filter(login_require=False)
        post = get_object_or_404(posts, pk=id)
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        posts = Post.objects.filter(status=True, published_date__lte=timezone.now())
        if not request.user.is_authenticated:
            posts = posts.filter(login_require=False)
        post = get_object_or_404(posts, pk=id)
        post.delete()
        return Response({'detail': 'item removed successfully'}, status=status.HTTP_204_NO_CONTENT)