from posts.models import Post
from django.db.models import Q
import json
from rest_framework.generics import (ListAPIView,RetrieveAPIView,\
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)
from .serializers import PostListSerializer,PostUpdateSerializer,PostCreateSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from .permissions import  IsOwnerOrReadOnly
from .pagination import PostLimitPagination,PostPageNumberPagination

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

class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class= PostCreateSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user) 


class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class= PostUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class= PostUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


