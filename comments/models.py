from django.db import models
import uuid
from posts.models import Post
from user.models import User

class Comments(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content=models.TextField(null=False,blank=False)
    post=models.ForeignKey(Post,related_name="post_comments",on_delete=models.CASCADE)
    author=models.ForeignKey(User,related_name="user_comments",on_delete=models.CASCADE)

    isVerified=models.BooleanField(default=False)
    isHidden=models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)



class Reply(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content=models.TextField(null=False,blank=False)
    comment=models.ForeignKey(Comments,related_name="comment_replies",on_delete=models.CASCADE)
    author=models.ForeignKey(User,related_name="user_replies",on_delete=models.CASCADE)
    
    isVerified=models.BooleanField(default=False)
    isHidden=models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)