from django.urls import  path,include
from .views import CommentListView,CommentDetail,CommentCreateView,CommentReplyListView
urlpatterns = [
    path('',CommentListView.as_view(),name = 'api_list_comments'),
    path('add_comment/',CommentCreateView.as_view(),name = 'api_add_comment'),
    path('<int:pk>/',CommentDetail.as_view(),name = 'api_comment_detail'),
    path('<int:pk>/replies/',include(('comments.api.reply_urls','comments.api'),namespace='comments-reply-api')),
]
