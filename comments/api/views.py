
from rest_framework.generics import (ListAPIView,RetrieveAPIView,\
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView)
from .serializers import CommentsSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from comments.models import Comment   

class CommentListView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer

class CommentDetail(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class= CommentsSerializer