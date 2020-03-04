from rest_framework.serializers import (ModelSerializer,
                                        HyperlinkedIdentityField,
                                        SerializerMethodField)
from posts.models import Post,Like
from rest_framework import  status
from rest_framework.reverse import reverse
from django.conf import  settings
User = settings.AUTH_USER_MODEL
import json
import requests
from accounts.models import  Account 
class PostListSerializer(ModelSerializer):
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
    liked = SerializerMethodField()
    likes = SerializerMethodField()
    viewLikes = HyperlinkedIdentityField(
        view_name='insta-api:post_likes_api',
        lookup_field='pk'
    )
    class Meta:
        model = Post
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
            'liked',
            'likes',
            'viewLikes'
        ]
    
    def get_likes(self,obj):
        return obj.like_set.count()
    def get_userProfileImage(self,obj):
        return obj.user.account.get_image_url()
    def get_userName(self,obj):
        return str(obj.user.username)
    def get_userProfileUrl(self,obj):
        return obj.user.account.get_full_url()
    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            liked = Like.objects.filter(account = user.account, post= obj);
            print(liked)
            if liked:
                return True
            else:
                return False
        else:
            return False

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
            'caption',
            'updated',
        ]
    
class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['created']
class UsersLikedPostSerializer(ModelSerializer):
    userName = SerializerMethodField()
    urlToProfile = SerializerMethodField()
    userProfileImage = SerializerMethodField()

    class Meta:
        model = Like
        fields = ['userName','userProfileImage','urlToProfile']
    
    def get_userName(self, obj):
        return obj.account.user.username
    def get_email(self, obj):
        return obj.account.user.email
    def get_userProfileImage(self,obj):
        return obj.accoutn.get_image_url
    def get_urlToProfile(self,obj):
        return obj.account.get_full_url()