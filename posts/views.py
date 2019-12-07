from django.shortcuts import render, HttpResponse
from .models import Post
def posts(request):
    posts = Post.objects.all()
    context ={
        'posts':posts,
    }
    return render(request,'posts/post_list.html',context)


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    context  = {
        'post':post,
    }
    return render(request,'posts/post_detail.html',context)
