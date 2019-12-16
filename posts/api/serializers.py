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
    likes = SerializerMethodField()
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
            'likes',
        ]
    
    def get_likes(self,obj):
        return obj.like_set.count()
    def get_userProfileImage(self,obj):
        if settings.DEBUG:
            domain = '127.0.0.1:8000'
        else:
            domain=None #WILL BE CHOOSE LATER 
        account = obj.user.account
        path = account.image.url 
        url = 'http://{}{}'.format(domain,path)
        return url
    def get_userName(self,obj):
        return str(obj.user.username)
    def get_userProfileUrl(self,obj):
        if settings.DEBUG:
            domain = '127.0.0.1:8000'
        else:
            domain=None #WILL BE CHOOSE LATER 
        account = obj.user.account
        path = account.get_absolute_url()
        url = 'http://{}{}'.format(domain,path)
        return url

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
