from django.db import models
from posts.models import Post
from django.conf import settings
from accounts.models import Account
# Create your models here.
class NewsFeedPost(models.Model):
    user = models.ForeignKey(Account,on_delete =  models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


# def add_to_newsfeed(sender, instance, created, **kwargs):
#     if created:
#         NewsFeed.objects.create(post = instance)
#         print('added to news feed')

# def update_to_newsfeed(sender, instance, created, **kwargs):
#     if not created:
#         instance.newsfeed.save()
#         print('updated')



    