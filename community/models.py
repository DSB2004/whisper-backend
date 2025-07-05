from django.db import models
import uuid
# Create your models here.


    
class Community(models.Model):
    from user.models import User
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    name=models.TextField(null=False,blank=False)
    summary=models.TextField(null=False,blank=False)
    members = models.ManyToManyField(User, related_name='joined_communities', blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

class CommunityTopics:
    from posts.models import TopicType
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community=models.ForeignKey(Community,related_name="community_related_topics",on_delete=models.CASCADE)
    topic=models.CharField(
        max_length=10,
        choices=TopicType.choices,
        blank=True,
        null=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

class CommunityAssets(models.Model):
    from posts.models import AssetsType
    from user.models import User
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    src=models.URLField(blank=False,null=False)
    name=models.TextField()
    community=models.ForeignKey(Community,related_name="post_assets",on_delete=models.CASCADE)
    type=models.CharField(
        max_length=10,
        choices=AssetsType.choices,
        default=AssetsType.OTHER
    )

    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

