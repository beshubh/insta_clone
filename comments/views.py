from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from posts.models import Post
from .models import Comment,Reply
User = get_user_model()
def add_comment(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            post = Post.objects.get(id=id)
            print(request.POST)
            text = request.POST['comment']
            comment = Comment.objects.create(user = user,post=post,text=text)
            comment.save()
            return redirect('post_list')

    else:
        return redirect('post_list')


def add_reply(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            parent_comment = Comment.objects.get(id=id)
            text = request.POST['reply'] 
            reply = Reply.objects.create(parent_comment=parent_comment,text=text)
            reply.save()
            return redirect('post_list')
