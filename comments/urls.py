from django.urls import  path
from . import views
urlpatterns = [
    path('<int:id>/add_comment',views.add_comment,name = 'add_comment'),
    path('<int:id>/add_reply',views.add_reply,name = 'add_reply'),
]