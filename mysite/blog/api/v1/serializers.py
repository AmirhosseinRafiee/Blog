from rest_framework import serializers
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from ...models import Post

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'image', 'title', 'content', 'category', 'tags', 'counted_view', 'created_date')
