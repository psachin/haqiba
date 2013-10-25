from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CodeTemplate(models.Model):
    name = models.CharField(max_length=128, unique=True)
    code = models.TextField()
    screenshot = models.ImageField(upload_to='screenshot', blank=True)

    def __unicode__(self):
        return self.name


