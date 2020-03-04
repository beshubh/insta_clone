from posts.models import Post
from django.db.models import Q
import json
from rest_framework.generics import (
    ListAPIView,RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
)

from .serializers import (
    PostListSerializer,
    PostUpdateSerializer,
    PostCreateSerializer,
    PostLikeSerializer,
    UsersLikedPostSerializer
)
from newsfeed.api.serializers import NewsFeedPostListSerializer
from accounts.api.serializers import UserListSerializer
from rest_framework.permissions import (
    AllowAny,   
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework import status
from .permissions import  IsOwnerOrReadOnly
from .pagination import PostLimitPagination,PostPageNumberPagination
from posts.models import Like
from accounts.models import Follower
from newsfeed.models import NewsFeedPost
from django.contrib.auth import get_user_model
User = get_user_model()


from rest_framework.parsers import JSONParser,FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

class PostCreateView(APIView):
    """
    A view that can accept POST requests with JSON content.
    """
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        account = user.account
        caption = request.data['caption']
        image = request.data['file']
        post = Post.objects.create(user =user, caption = caption, image = image)
        post.save()
        return Response({
            'success': True,
            'message':'Uploaded successfully'
        })

# This view lists all the post 
class PostListView(ListAPIView):
    serializer_class = PostListSerializer
    permisson_classes = [AllowAny]
    pagination_class = PostPageNumberPagination
    def get_queryset(self, *args,**kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(caption__icontains=query)|
                Q(user__username__icontains=query)
            ).distinct()

        return queryset_list

# This view will list all the post create by specific user
# class UserPostListView(ListAPIView):
#     serializer_class = PostListSerializer
#     permission_classes = [AllowAny]
#     pagination_class = PostPageNumberPagination
#     def get_queryset(self,*args, **kwargs):
#         pk = kwargs['pk']


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class= PostListSerializer    
# View for creating new post
# class PostCreateView(CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class= PostCreateSerializer
#     permission_classes = [IsAuthenticated]
#     def perform_create(self,serializer):
#         serializer.save(user=self.request.user)
#This view is used to update the post 
class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class= PostUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

# This view is used to delete the post
class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class= PostUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# This View is used to like the post
class PostLikeCreateView(CreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, pk,format=None):
        user = self.request.user
        post_ = Post.objects.get(id=self.kwargs['pk'])
        try:
            like = Like.objects.get(account=user.account,post=post_)
        except:
            like = None
        if not like:
            serializer = PostLikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(account=user.account,post=post_)
                return Response({
                    'message':'LIKED',
                    'status' : status.HTTP_201_CREATED,
                })
            else:
                return Response({
                    'error': serializer.errors,
                    'status':tatus.HTTP_400_BAD_REQUEST
                })
        
        else:
            like.delete()
            return Response({
                'message':'DISLIKED',
                'status':status.HTTP_200_OK
            })
        


# This view is used to get all the users who like the post         
class PostLikeListView(ListAPIView):
    serializer_class = UsersLikedPostSerializer
    def get_queryset(self, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        queryset = post.like_set.all()
        return queryset
        
from datetime import date
today = date.today()

class HomeView(ListAPIView):
    serializer_class = NewsFeedPostListSerializer
    # queryset = NewsFeedPost.objects.all()
    permission_classes = [IsAuthenticated]
    def get_queryset(self,*args,**kwargs):
        user = User.objects.get(pk = self.request.user.id)
        print(user)
        print(self.request)
        print(self.request.headers)
        print(self.request.data)
        account = user.account
        queryset = NewsFeedPost.objects.filter(user=account)
        return queryset
            # else:
            #     return Response({
            #         'message':'You do not following any one','status':status.HTTP_204_NO_CONTENT})
        # else:
        #     return Response({
        #         'success':False,
        #         'message':'Not Authenticated',
        #         'status':status.HTTP_203_NON_AUTHORITATIVE_INFORMATION
        #         })

