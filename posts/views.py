from django.shortcuts import render, HttpResponse

def posts(request):
    return HttpResponse('post list')