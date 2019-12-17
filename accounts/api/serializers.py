
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import Account,Follower
from django.conf import  settings
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )

# Register
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password')
        extra_kwargs = {'password':{'write_only':True}}
    def create(self, validated_data):
        print('creating user')
        user = User.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password'])
        account = Account.objects.create(user=user)
        account.save()
        print('created')
        return user


# Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        else:
            raise serializers.ValidationError('Incorrect Credentials')

class UserListSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    urlToProfile = serializers.HyperlinkedIdentityField(
        view_name='accounts-api:api_account_detail',
        lookup_field = 'pk',
    )
    # userProfileImage =serializers. SerializerMethodField()    
    class Meta:
        model = Account
        fields = ['userName','email','image','urlToProfile']
    def get_userName(self, obj):
        return obj.user.username
    def get_email(self, obj):
        return obj.user.email
    def get_userProfileImage(self,obj):
        return obj.get_image_url()
class UserDetailSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    class Meta:
        model = Account
        fields = ['userName','email','image']
    def get_userName(self,obj):
        return str(obj.user.username)
    def get_email(self,obj):
        return obj.user.email
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['on']
class FollowersListSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    userProfileImage = serializers.SerializerMethodField()
    urlToProfile = serializers.SerializerMethodField()
    class Meta:
        model = Follower
        fields = ['userName','userProfileImage','urlToProfile']
    def get_userName(self,obj):
        return str(obj.following_user.username)
    def get_userProfileImage(self,obj):
        return obj.following_user.account.get_image_url()
    def get_urlToProfile(self,obj):
        return obj.following_user.account.get_full_url()
class FollowingListSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    userProfileImage = serializers.SerializerMethodField()
    urlToProfile = serializers.SerializerMethodField()
    class Meta:
        model = Follower
        fields = ['userName','userProfileImage','urlToProfile']
    def get_userName(self,obj):
        return str(obj.followed_user.username)
    def get_userProfileImage(self,obj):
        return obj.followed_user.account.get_image_url()
    def get_urlToProfile(self,obj):
        return obj.followed_user.account.get_full_url()
        