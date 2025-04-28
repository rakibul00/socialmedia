from django.contrib import admin
from .models import CustomUser, Friendship, Story, Post, Like, Comment
admin.site.register(CustomUser),
admin.site.register(Friendship),
admin.site.register(Story),
admin.site.register(Post),
admin.site.register(Like),
admin.site.register(Comment),
# Register your models here.
