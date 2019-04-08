from django.db import models

# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=100)