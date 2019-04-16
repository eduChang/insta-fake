from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Hashtag(models.Model):
    content = models.CharField(max_length=100)
    
    def __str__(self):
        return self.content
class Post(models.Model):
    content = models.CharField(max_length=100)
    # image = models.ImageField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_post_set", blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    
class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = ProcessedImageField(
                upload_to='posts/images', #저장 위치
                processors=[ResizeToFill(600,600)], #크기지정
                format='JPEG',
                options={'quality':90},
        )
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta():
        ordering = ['-created_at']
# class Like(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    
    
    
    
    
    
    
    
    