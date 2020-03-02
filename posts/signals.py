from django.db.models.signals import post_save
from .models import Post

def add_post_to_followers_newsfeed(sender, instance,**kwargs):
    print('yes it is running')
    print(instance)
    print(sender)
