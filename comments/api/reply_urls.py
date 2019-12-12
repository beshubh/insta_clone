from django.urls import  path
from .views import CommentReplyListView,CommentReplyCreateView
urlpatterns = [
    path('',CommentReplyListView.as_view(),name='api_comment_replies'),
    path('add_reply',CommentReplyCreateView.as_view(), name='api_add_comment_reply')
]
