
from rest_framework.generics import (ListAPIView,RetrieveAPIView,\
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView
    )
from .serializers import CommentsSerializer,CommentCreateSerializer,CommentsReplySerializer,CommentReplyCreateSerializer
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from comments.models import Comment   
from posts.models import Post

# View for listing all the comment of a particular post
class CommentListView(APIView):
    def get(self, request, pk, format=None):
        post = Post.objects.get(id=pk)
        queryset_list = post.comment_set.all()
        context = {'request':request}
        serializer = CommentsSerializer(queryset_list,many=True,context = context)
        return Response(serializer.data)

# View for single comment
class CommentDetail(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class= CommentsSerializer


# View for creating the comment
class CommentCreateView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        print(pk)
        pst = Post.objects.get(id = pk)
        print(pst)
        user = request.user
        print(request.data)
        serializer = CommentCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(post = pst, user = user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# View for getting all the replies of a particular comment
class CommentReplyListView(APIView):
    def get(self, request,format=None,*args,**kwargs):
        comment_id = kwargs['pk']
        comment = Comment.objects.get(id=comment_id)
        queryset_list = comment.reply_set.all()
        serializer = CommentsReplySerializer(queryset_list,many=True)
        return Response(serializer.data)
        
# View for creating the reply to certain comment
class CommentReplyCreateView(CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, pk, format=None):
        print(pk)
        parent_comment = Comment.objects.get(id = pk)
        user = request.user
        print(request.data)
        serializer = CommentReplyCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(parent_comment = parent_comment, user = user)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
