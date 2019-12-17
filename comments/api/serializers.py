from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        HyperlinkedIdentityField,
                                        )
        
from comments.models import Comment,Reply

class CommentsSerializer(ModelSerializer):
    userName = SerializerMethodField()
    urlToProfile = SerializerMethodField()
    urlToProfileImage = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'post',
            'userName',
            'urlToProfileImage',
            'urlToProfile',
            'text',
            'timestamp',
        ]
    def get_userName(self,obj):
        return obj.user.username
    def get_urlToProfile(self,obj):
        url = obj.user.account.get_full_url()
        return url
    def get_urlToProfileImage(self, obj):
        url_to_image = obj.user.account.get_image_url()
        return url_to_image
class CommentCreateSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'text',
            'timestamp',
        ]

class CommentReplyCreateSerializer(ModelSerializer):

    class Meta:
        model = Reply   
        fields = [
            'text',
            'timestamp',
        ]
class CommentsReplySerializer(ModelSerializer):
    user = SerializerMethodField()
    class Meta:
        model = Reply
        fields = [
            'user',
            'text',
            'timestamp',
        ]
    def get_user(self, obj):
        return str(obj.user)