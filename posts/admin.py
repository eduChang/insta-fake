from django.contrib import admin
from .models import Post,Image, Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
