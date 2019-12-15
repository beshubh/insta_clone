from django.urls import path, include
from .views import RegisterApiView,LoginApiView,UserApiView
from knox import views as knox_views    

urlpatterns =[
    path('auth/',include('knox.urls')),
    path('auth/register',RegisterApiView.as_view(),name='api_register'),
    path('auth/login',LoginApiView.as_view(),name='api_login'),
    path('auth/user',UserApiView.as_view(),name='api_user'),
     path('auth/logout',knox_views.LogoutView.as_view(),name='api_logout'), 
]