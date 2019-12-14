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
    PostLikeSerializer
)

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

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class= PostListSerializer

# View for creating new post
class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class= PostCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user) 

#
class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class= PostUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class= PostUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class PostLikeCreateView(CreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, pk,format=None):
        user = self.request.user
        post_ = Post.objects.get(id=self.kwargs['pk'])
        try:
            like = Like.objects.get(user=user,post=post_)
        except:
            like = None
        if not like:
            serializer = PostLikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user,post=post_)
                return Response('LIKED', status = status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            like.delete()
            return Response('DISLIKED')
        

        
        