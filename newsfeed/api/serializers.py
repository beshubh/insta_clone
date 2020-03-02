from rest_framework.serializers import ModelSerializer,SerializerMethodField, HyperlinkedIdentityField
from rest_framework import status
from ..models import NewsFeedPost

class NewsFeedPostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name = 'insta-api:post_detail_api',
        lookup_field ='pk',
    )
    userProfileImage = SerializerMethodField()
    userName = SerializerMethodField()
    userProfileUrl = SerializerMethodField()
    comments = HyperlinkedIdentityField(
        view_name='comments-api:api_list_comments',
        lookup_field='pk',
    )
    likes = SerializerMethodField()
    timestamp = SerializerMethodField()
    updated = SerializerMethodField()
    image = SerializerMethodField()
    caption = SerializerMethodField()
    viewLikes = HyperlinkedIdentityField(
        view_name='insta-api:post_likes_api',
        lookup_field='pk'
    )
    class Meta:
        model = NewsFeedPost
        fields = [
            'url',
            'userProfileImage',
            'userName',
            'userProfileUrl',
            'image',
            'caption',
            'timestamp',
            'updated',
            'comments',
            'likes',
            'viewLikes'
        ]
    def get_image(self, obj):
        return obj.post.image.url
    def get_likes(self,obj):
        return obj.post.like_set.count()
    def get_userProfileImage(self,obj):
        return obj.post.user.account.get_image_url()
    def get_userName(self,obj):
        return str(obj.post.user.username)
    def get_userProfileUrl(self,obj):
        return obj.post.user.account.get_full_url()
    def get_timestamp(self,obj):
        return obj.post.timestamp
    def get_updated(self,obj):
        return obj.post.updated
    def get_caption(self, obj):
        return obj.post.caption