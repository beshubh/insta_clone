from django.db import models
from django.conf import settings
from accounts.models import Account
def upload_location(instance, filename):
    return 'posts/{}/{}'.format(instance, filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_location)
    caption = models.CharField(max_length = 250)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    

    def __str__(self):
        return self.caption
    class Meta:
        ordering=['-timestamp']




class Like(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return self.account.user.username