from django.db import models
import uuid
from user.models import User

class AssetsType(models.TextChoices):
    IMG = "IMG", "Images"
    AUDIO = "AUDIO", "Audio"
    VIDEO = "VIDEO", "Video"
    OTHER ="OTHER",'Other'



class Post(models.Model): 
    from user.models import User
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    title=models.TextField(blank=False,null=False)
    body=models.TextField(blank=False,null=False)
    
    isVerified=models.BooleanField(default=False)
    isHidden=models.BooleanField(default=False)
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)




class Assets(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    src=models.URLField(blank=False,null=False)
    name=models.TextField()
    post=models.ForeignKey(Post,related_name="post_assets",on_delete=models.CASCADE)
    type=models.CharField(
        max_length=10,
        choices=AssetsType.choices,
        default=AssetsType.OTHER
    )


    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)



