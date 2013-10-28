from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CodeTemplate(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128, unique=True)
    code = models.TextField()
    description = models.TextField()
    screenshot = models.ImageField(upload_to='screenshot', blank=True)
    download_count = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    # this line is req. links userprofile to a user model instance
    user = models.OneToOneField(User)
    
    # additional attributes
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_image', blank=True)
    
    # unicode stuf
    def __unicode__(self):
        return self.user.username
