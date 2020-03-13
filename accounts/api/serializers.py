
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import Account,Follower
from django.conf import  settings
# from newsfeed.models import NewsFeed
from posts.models import Post
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

class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    class Meta:
        model = Account
        fields = ('id','username', 'image','email')
    
    def get_username(self,obj):
        return obj.user.username
    def get_email(self, obj):
        return obj.user.email

    


class UserListSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    follows = serializers.SerializerMethodField()
    # userProfileImage =serializers. SerializerMethodField()    
    class Meta:
        model = Account
        fields = ['userName','id','email','image','follows']
    def get_userName(self, obj):
        return obj.user.username
    def get_email(self, obj):
        return obj.user.email
    def get_userProfileImage(self,obj):
        return obj.get_image_url()
    def get_follows(self, obj):
        following_user = self.context['request'].user
        followed_user = obj.user
        follows = None
        try:
            follows = Follower.objects.get(following_user =following_user, followed_user = followed_user)
        except:
            follows = None
        if follows:
            return True
        return False
class SearchUsersListSerializer(serializers.ModelSerializer):
    follows = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    

    class Meta:
        model = User
        fields = ['username','user_id','email','image','follows']
    
    def get_image(self,obj):
        return obj.account.get_image_url()
    def get_user_id(self,obj):
        return obj.id
    def get_follows(self, obj):
        following_user = self.context['request'].user
        followed_user = obj
        follows = None
        try:
            follows = Follower.objects.get(following_user =following_user, followed_user = followed_user)
        except:
            follows = None
        if follows:
            return True
        return False
    
class UserDetailSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    follows = serializers.SerializerMethodField()
    class Meta:
        model = Account
        fields = ['userName','user_id','email','image','follows','followers','following']
    def get_userName(self,obj):
        return str(obj.user.username)
    def get_email(self,obj):
        return obj.user.email
    def get_followers(self, obj):
        user = obj.user
        followers = Follower.objects.filter(followed_user = user).count()
        return followers
    def get_following(self, obj):
        user = obj.user
        following = Follower.objects.filter(following_user = user).count()
        return following
    def get_user_id(self, obj):
        return obj.id
    def get_follows(self, obj):
        following_user = self.context['request'].user
        followed_user = obj.user
        follows = None
        try:
            follows = Follower.objects.get(following_user =following_user, followed_user = followed_user)
        except:
            follows = None
        if follows:
            return True
        return False





class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['on']
class FollowersListSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    userProfileImage = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    follows = serializers.SerializerMethodField()
    class Meta:
        model = Follower
        fields = ['userName','follows','user_id','userProfileImage']
    def get_userName(self,obj):
        return str(obj.following_user.username)
    def get_userProfileImage(self,obj):
        return obj.following_user.account.get_image_url()
    def get_user_id(self, obj):
        return obj.following_user.account.id
    def get_follows(self, obj):
        following_user = self.context['request'].user
        followed_user = obj.following_user
        follows = None
        try:
            follows = Follower.objects.get(following_user =following_user, followed_user = followed_user)
        except:
            follows = None
        if follows:
            return True
        return False

class FollowingListSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    userProfileImage = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    follows = serializers.SerializerMethodField()
    class Meta:
        model = Follower
        fields = ['userName','user_id','follows','userProfileImage']
    def get_userName(self,obj):
        return str(obj.followed_user.username)
    def get_userProfileImage(self,obj):
        return obj.followed_user.account.get_image_url()
    def get_user_id(self, obj):
        return obj.followed_user.account.id
    def get_follows(self,obj):
        following_user = self.context['request'].user
        followed_user = obj.followed_user
        try:
            follows = Follower.objects.get(following_user =following_user, followed_user = followed_user)
        except:
            follows = None
        if follows:
            return True
        return False

        