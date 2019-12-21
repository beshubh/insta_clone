from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework import status
from .serializers import (UserSerializer,RegisterSerializer,
                         LoginSerializer,UserListSerializer,
                         FollowSerializer,FollowersListSerializer,
                         FollowingListSerializer,
                         UserDetailSerializer,
)
from django.contrib.auth.models import User
from accounts.models import Account ,Follower
# Register API
class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user':UserSerializer(user,context =self.get_serializer_context()).data,
            'token':AuthToken.objects.create(user)[1],  
        })

# Login API
class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(    raise_exception=True)
        user = serializer.validated_data
        return Response({
            'user':UserSerializer(user,context =self.get_serializer_context()).data,
            'token':AuthToken.objects.create(user)[1],  
        })

# Get User API
class UserApiView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    queryset = Account.objects.all()

class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer 
    queryset = Account.objects.all()

class FollowUserView(generics.CreateAPIView):
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
        if not follow:
            serializer = FollowSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(following_user=following_user,followed_user = followed_user)
                return Response('You followed {}'.format(followed_user.username), status = status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response('You already follow {}'.format(followed_user.username),status.HTTP_200_OK)
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
            return Response('You unfollowed {}'.format(followed_user.username),status.HTTP_202_ACCEPTED)
        
        else:
            return Response('You does not follow {}'.format(followed_user.username),status.HTTP_200_OK)
        
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
