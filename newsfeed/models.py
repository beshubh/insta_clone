from django.db import models
from posts.models import Post
from django.conf import settings
from accounts.models import Account,Follower
from django.db.models.signals import post_save
# Create your models here.
class NewsFeedPost(models.Model):
    user = models.ForeignKey(Account,on_delete =  models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


def add_to_newsfeed(sender, instance, created, **kwargs):
    if created:
        post_user = instance.user
        followers = Follower.objects.filter(followed_user = post_user)
        for user in followers:
            print('creating ....')
            NewsFeedPost.objects.create(user=user.following_user.account,post=instance)
            print('created')

            

post_save.connect(add_to_newsfeed,sender=Post)

def update_to_newsfeed(sender, instance, created, **kwargs):
    if not created:
        instance.newsfeed.save()
        print('updated')



    