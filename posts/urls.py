from django.urls import path
from . import views


urlpatterns = [
    path('',views.posts,name='post_list'),
    path('<int:pk>/',views.post_detail, name='post_detail'),
    path('add_post/',views.add_post, name='add_post')   
]