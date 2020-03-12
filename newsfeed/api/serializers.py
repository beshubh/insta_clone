from rest_framework.serializers import ModelSerializer,SerializerMethodField, HyperlinkedIdentityField
from rest_framework import status
from ..models import NewsFeedPost
from posts.models import Like
class NewsFeedPostListSerializer(ModelSerializer):
    id = SerializerMethodField()
    url = SerializerMethodField()
    userProfileImage = SerializerMethodField()
    userName = SerializerMethodField()
    user_id = SerializerMethodField()
    likes = SerializerMethodField()
    timestamp = SerializerMethodField()
    updated = SerializerMethodField()
    image = SerializerMethodField()
    caption = SerializerMethodField()
    liked = SerializerMethodField()
    class Meta:
        model = NewsFeedPost
        fields = [
            'id',
            'url',
            'userProfileImage',
            'userName',
            'user_id',
            'image',
            'caption',
            'timestamp',
            'updated',
            'liked',
            'likes',
        ]
    def get_id(self, obj):
        return obj.post.id
    def get_url(self, obj):
        return obj.post.get_full_url();
    def get_image(self, obj):
        return obj.post.get_full_image_url()
    def get_likes(self,obj):
        print(obj.post)
        print(obj.post.like_set.count())
        print(obj.post.like_set)
        return obj.post.like_set.count()
    def get_userProfileImage(self,obj):
        return obj.post.user.account.get_image_url()
    def get_userName(self,obj):
        return str(obj.post.user.username)
    def get_user_id(self,obj):
        return obj.post.user.account.id
    def get_timestamp(self,obj):
        return obj.post.timestamp
    def get_updated(self,obj):
        return obj.post.updated
    def get_caption(self, obj):
        return obj.post.caption
    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            liked = Like.objects.filter(account = user.account, post= obj.post);
            if liked:
                return True
            else:
                return False
        else:
            return False