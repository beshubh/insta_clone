from rest_framework.serializers import (ModelSerializer,
                                        HyperlinkedIdentityField,
                                        SerializerMethodField)
from posts.models import Post

class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name = 'insta-api:post_detail_api',
        lookup_field ='pk',
    )
    user = SerializerMethodField()
    comments = HyperlinkedIdentityField(
        view_name='comments-api:api_list_comments',
        lookup_field='pk',
    )
    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'image',
            'caption',
            'timestamp',
            'updated',
            'comments',
        ]
    def get_user(self, obj):
        return str(obj.user.username)



class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'image',
            'caption',
        ]


class PostDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'user',
            'image',
            'caption',
            'timestamp',
            'updated',
        ]
    def get_user(self, obj):
        return str(obj.user.username)
    def get_image(self, obj):
        try:
            image = obj.image.url 
        except:
            image = None
        return image


class PostUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'image',
            'caption',
            'timestamp',
            'updated',
        ]
    