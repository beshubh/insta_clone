from django.urls import path, include
from .views import (RegisterApiView,LoginApiView,
                    UserApiView,UserListView,UserDetail,
                    FollowersList,FollowUserView,
                    FollowingList,UnFollowUserView
                    )
from knox import views as knox_views    

urlpatterns =[
    path('auth/',include('knox.urls')),
    path('auth/register',RegisterApiView.as_view(),name='api_register'),
    path('auth/login',LoginApiView.as_view(),name='api_login'),
    path('auth/user',UserApiView.as_view(),name='api_user'),
    path('auth/logout',knox_views.LogoutView.as_view(),name='api_logout'), 
    path('auth/users',UserListView.as_view(),name='api_users_list'),
    path('auth/users/<int:pk>',UserDetail.as_view(),name='api_user_detail'),
    path('auth/users/<int:pk>/follow',FollowUserView.as_view(),name='api_user_follow'),
    path('auth/users/<int:pk>/unfollow',UnFollowUserView.as_view(),name='api_user_unfollow'),
    path('auth/users/<int:pk>/followers',FollowersList.as_view(),name='api_user_followers'),
    path('auth/users/<int:pk>/following',FollowingList.as_view(),name='api_user_following'),
]