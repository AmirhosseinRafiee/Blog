from rest_framework import serializers
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from accounts.models import Profile
from ...models import Post, Category

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'id')
        read_only_fields = ('id',)

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'image')
        read_only_fields = ('first_name', 'last_name', 'image')

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(slug_field='name', many=True, queryset=Category.objects.all())
    # category = CategorySerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'image', 'title', 'content', 'snippet', 'relative_url', 'absolute_url', 'category', 'tags', 'counted_view', 'published_date')
        read_only_fields = ('id', 'author', 'counted_view')
    
    def get_absolute_url(self, post):
        request = self.context.get('request')
        return request.build_absolute_uri(post.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep =  super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category, many=True).data
        rep['author'] = AuthorSerializer(instance.author).data
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('snippet', None)
            rep.pop('relative_url', None)
            rep.pop('absolute_url', None)
        else:
            rep.pop('content', None)
        return rep
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = Profile.objects.get(user=request.user.id)
        return super().create(validated_data)
