from django.db import models
from django.conf import settings
from posts.models import Post
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    

    def __str__(self):
        return self.text 
    


class Reply(models.Model):
    parent_comment = models.ForeignKey(Comment,on_delete=models.CASCADE)   
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True, blank=True) 
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.text