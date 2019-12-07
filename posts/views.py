from django.shortcuts import render, HttpResponse,redirect
from django.contrib import  messages
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


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            image = request.FILES['post_image']
            caption = request.POST['post_caption']
            new_post = Post.objects.create(user=request.user, image = image, caption = caption)
            new_post.save()
            return redirect('post_list')
        else:
            return render(request, 'posts/add_post.html')

    else:
        messages.error(request,'You need to login first')
        return redirect('post_list')