from django.db import models
from django.contrib.auth.models import User

# Local imports
from human_readable_size import hr_size


# Create your models here.
class CodeTemplate(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128, unique=True)
    gist_url = models.URLField(max_length=70, blank=True, null=True)
    code = models.TextField()
    description = models.TextField()
    screenshot = models.ImageField(upload_to='screenshot', blank=True)
    download_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def human_readable_download_count(self):
        return hr_size(self.download_count)


class Dependency(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    loadpath = models.BooleanField(default=True)
    require = models.BooleanField(default=True)
    tarFile = models.FileField(upload_to='deps', blank=True)
    config = models.TextField(blank=True)
    screenshot = models.ImageField(upload_to='screenshot', blank=True)
    download_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def human_readable_download_count(self):
        return hr_size(self.download_count)


class BundleTemplate(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField()
    dep = models.ManyToManyField(Dependency)
    config = models.TextField(blank=True)
    screenshot = models.ImageField(upload_to='screenshot', blank=True)
    download_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def human_readable_download_count(self):
        return hr_size(self.download_count)


class UserProfile(models.Model):
    # this line is req. links userprofile to a user model instance
    user = models.OneToOneField(User)

    # additional attributes
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_image', blank=True)

    # unicode stuff
    def __unicode__(self):
        return self.user.username
