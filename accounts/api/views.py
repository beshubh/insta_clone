from rest_framework import generics, permissions
from rest_framework.serializers import HyperlinkedIdentityField
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import status
from .serializers import (UserSerializer,RegisterSerializer,
                         LoginSerializer,UserListSerializer,
                         FollowSerializer,FollowersListSerializer,
                         FollowingListSerializer,UpdateProfileSerializer,
                         UserDetailSerializer,SearchUsersListSerializer
)

from django.contrib.auth.models import User
from accounts.models import Account ,Follower
from posts.api.serializers import PostListSerializer
from posts.api.pagination import PostLimitPagination
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from posts.models import Post
from .permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import APIException
from django.http import JsonResponse
# Register API
class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request,*args,**kwargs):
        print(request)
        print(request.data)
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'success':True,
            'user':UserSerializer(user,context =self.get_serializer_context()).data,
            'token':AuthToken.objects.create(user)[1],  
        })

# Login API
class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        auth_token = AuthToken.objects.create(user);
        token  = auth_token[1]
        print(token)
        return Response({
            'sucess':True,
            'user':UserSerializer(user,context =self.get_serializer_context()).data,
            'token':token,  
        })
# Update profile
class EditProfileView(generics.GenericAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        if user == request.user:
            account = user.account
            username = None
            temp_user = None
            email = None
            image = None
            try:
                username = request.data['username']
            except:
                username = None
            try:
                temp_user = User.objects.get(username = username)
            except:
                temp_user = None
            try:
                email = request.data['email']
            except:
                email = None
            try:
                image = request.data['image']
            except:
                image = None
            user.username =username or user.username
            user.email = email or user.email
            account.image = image or account.image
            user.save()
            account.save()
            return Response({"success":True,"detail":"Profile Updated successfully"})
        else:
            return Response({"success":False,"detail":"You are not allowed to do this operation"})


# Get User API
class UserApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user
        

class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = Account.objects.all()

class SearchUsersListview(generics.ListAPIView):
    serializer_class = SearchUsersListSerializer
    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        queryset = User.objects.filter(username__icontains = query)
        return queryset    

class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer 
    queryset = Account.objects.all()

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        user = request.user
        account = request.user.account
        image = account.get_image_url()
        username = user.username
        user_id = user.id
        email = user.email
        followers = Follower.objects.filter(followed_user = user).count()
        following = Follower.objects.filter(following_user = user).count()
        return Response({
            'username':username,
            'user_id':user_id,
            'email':email,
            'profileImage':image,
            'followers':followers,
            'following':following
        })
class ProfileFollowersView(generics.ListAPIView):
    serializer_class = FollowersListSerializer
    def get_queryset(self):
        user = self.request.user   
        queryset = Follower.objects.filter(followed_user = user)
        return queryset     
class ProfileFollowingView(generics.ListAPIView):
    serializer_class = FollowingListSerializer
    def get_queryset(self):
        user = self.request.user   
        queryset = Follower.objects.filter(following_user = user)
        return queryset  

class UserPostListView(ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    pagination_class = PostLimitPagination
    def get_queryset(self,*args, **kwargs):
        pk = self.kwargs['pk']
        print(pk)
        user = User.objects.get(pk=pk)
        queryset = user.post_set.all()
        return queryset

class FollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk,format=None):
        following_user = self.request.user
        id = int(pk)
        account = Account.objects.get(id=id)
        followed_user = account.user
        try:
            follow = Follower.objects.get(following_user=following_user,followed_user=followed_user)
        except:
            follow = None
        if not follow:
            serializer = FollowSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(following_user=following_user,followed_user = followed_user)
                return Response({
                    'success':True,
                    'message': 'You followed {}'.format(followed_user.username),
                    'status' : status.HTTP_202_ACCEPTED
                    })
            else:
                return Response({
                    'success':False,
                    'error':serializer.errors,
                    'status' : status.HTTP_400_BAD_REQUEST,
                    })
        
        else:
            return Response({
                'success':False,    
                'message':'You already follow {}'.format(followed_user.username),
                'status':status.HTTP_200_OK,
            })
class UnFollowUserView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk,format=None):
        following_user = self.request.user
        account = Account.objects.get(id=pk)
        followed_user = account.user
        try:
            follow = Follower.objects.get(following_user=following_user,followed_user=followed_user)
        except:
            follow = None
        if follow:
            follow.delete()
            return Response({
                'success':True,
                'message': 'You unfollowed {}'.format(followed_user.username),
                'status': status.HTTP_202_ACCEPTED
                })
        else:
            return Response({
                'success':False,
                'message':'You do not follow {}'.format(followed_user.username),
                'status':status.HTTP_400_BAD_REQUEST
            })
        
class FollowersList(generics.ListAPIView):
    serializer_class = FollowersListSerializer
    def get_queryset(self):
        account = Account.objects.get(id = self.kwargs['pk'])
        user = account.user
        queryset = Follower.objects.filter(followed_user = user)
        return queryset
class FollowingList(generics.ListAPIView):
    serializer_class = FollowingListSerializer
    def get_queryset(self):
        account = Account.objects.get(id=self.kwargs['pk'])
        user = account.user 
        queryset = Follower.objects.filter(following_user=user)
        return queryset


def check(request,un):
    try:
        user = User.objects.get(username = un)
    except:
        user = None

    if user:
        return JsonResponse({"success":False})
    else:
        return JsonResponse({"success":True})
        

    


