from django.urls import path, include
from .views import (RegisterApiView,LoginApiView,
                    UserApiView,UserListView,UserDetail,
                    FollowersList,FollowUserView,
                    FollowingList,UnFollowUserView,
                    ProfileView,ProfileFollowersView,
                    ProfileFollowingView,UserPostListView,
                    )
from knox import views as knox_views    

urlpatterns =[
    path('auth/',include('knox.urls')),
    path('auth/register',RegisterApiView.as_view(),name='api_register'),
    path('profile/',ProfileView.as_view(), name='api_profile'),
    path('profile/followers/',ProfileFollowersView.as_view(), name='api_profile_followers'),
    path('profile/following/',ProfileFollowingView.as_view(), name='api_profile_following'),
    path('auth/login/',LoginApiView.as_view(),name='api_login'),
    path('auth/user/',UserApiView.as_view(),name='api_user'),
    path('auth/logout/',knox_views.LogoutView.as_view(),name='api_logout'), 
    path('auth/accounts/',UserListView.as_view(),name='api_accounts_list'),
    path('auth/accounts/<int:pk>/',UserDetail.as_view(),name='api_account_detail'),
    path('auth/accounts/<int:pk>/posts/',UserPostListView.as_view(),name='api_account_detail_posts'),
    path('auth/accounts/<int:pk>/follow/',FollowUserView.as_view(),name='api_account_follow'),
    path('auth/accounts/<int:pk>/unfollow/',UnFollowUserView.as_view(),name='api_account_unfollow'),
    path('auth/accounts/<int:pk>/followers/',FollowersList.as_view(),name='api_account_followers'),
    path('auth/accounts/<int:pk>/following/',FollowingList.as_view(),name='api_account_following'),
]