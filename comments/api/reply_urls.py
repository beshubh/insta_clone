from django.urls import  path
from .views import CommentReplyListView
urlpatterns = [
    path('',CommentReplyListView.as_view(),name='api_comment_replies'),
]
