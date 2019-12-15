
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import Account,Follower

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
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    url_to_profile = serializers.HyperlinkedIdentityField(
        view_name='accounts-api:api_user_detail',
        lookup_field = 'pk',
    )
    class Meta:
        model = Account
        fields = ['username','email','image','url_to_profile']
    def get_username(self, obj):
        return obj.user.username
    def get_email(self, obj):
        return obj.user.email

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['on']
class FollowersListSerializer(serializers.ModelSerializer):
    following_user = serializers.SerializerMethodField()
    class Meta:
        model = Follower
        fields = ['following_user']
    def get_following_user(self,obj):
        return obj.following_user.username

class FollowingListSerializer(serializers.ModelSerializer):
    followed_user = serializers.SerializerMethodField()
    class Meta:
        model = Follower
        fields = ['followed_user']
    
    def get_followed_user(self, obj):
        return obj.followed_user.username
        