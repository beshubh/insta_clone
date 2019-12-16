from django.db import models
from django.conf import settings
from PIL import Image
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
    




class Follower(models.Model):
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,\
                                                related_name='following_user',null=True,blank=True)
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,\
                                                related_name='followed_user',null=True,blank=True)
    on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.following_user.username

# class Following(models.Model):
#     following_user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     followed_by_user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     on = models.DateTimeField(auto_now_add=True)
