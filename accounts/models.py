from django.db import models
from django.conf import settings
from PIL import Image
from rest_framework.reverse import reverse
from django.http import HttpRequest,request
from rest_framework.reverse import reverse_lazy
from django.conf import  settings
# from newsfeed.models import NewsFeedPost
def upload_location(instance, filename):
    return 'accounts/{}/{}'.format(instance, filename)


class Account(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_location,default='accounts/default.jpeg')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('accounts-api:api_account_detail',kwargs={'pk':self.pk})
    def get_full_url(self):
        domain = 'instaclone.pythonanywhere.com'
        path = self.get_absolute_url()
        return 'http://{}{}'.format(domain,path)
    def get_image_url(self):
        domain = 'instaclone.pythonanywhere.com'
        path = self.image.url
        return 'http://{}{}'.format(domain,path)


class Follower(models.Model):
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,\
                                                related_name='following_user',null=True,blank=True)
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,\
                                                related_name='followed_user',null=True,blank=True)
    on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.following_user.username

