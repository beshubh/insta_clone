from django.urls import  path
from .views import CommentListView,CommentDetail
urlpatterns = [
    path('',CommentListView.as_view(),name = 'list_comments'),
    path('<int:pk>/',CommentDetail.as_view(),name = 'api_comment_detail'),
]
