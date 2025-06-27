from django.db import models
import uuid
from user.models import User
from posts.models import Post
from comments.models import Comments,Reply
# Create your models here.


#  for post we can have saves reactions repost forwards 
#  for comments we can have reactions 
#  can also mark post as spam 

# can record the viewship 

class Reactions(models.TextChoices):
    THUMPS_UP = "THUMPS_UP", "Thumps up"
    HAPPY = "HAPPY", "Happy"
    LOVE = "LOVE", "Love"
    LAUGH ="LAUGH",'Laugh'
    CURIOUS ="CURIOS","Curious"
    CELEBRATE="CELEBRATE","Celebrate"




class PostReactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reaction")
    reactions=models.CharField(max_length=10,
        choices=Reactions.choices,
        default=Reactions.THUMPS_UP)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'post')

class CommentReactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name="post_reaction")
    reactions=models.CharField(max_length=10,
        choices=Reactions.choices,
        default=Reactions.THUMPS_UP)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'comment')

class ReplyReactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name="post_reaction")
    reactions=models.CharField(max_length=10,
        choices=Reactions.choices,
        default=Reactions.THUMPS_UP)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'reply')


class PostViewership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reaction")
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'post')

class PostViewtime(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reaction")
    createdAt = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(default=0.0)
    updateAt = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'post')

class PostReportDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reaction")
    reason = models.CharField(max_length=255, choices=[
        ("MISLEADING", "Misleading or scam"),
        ("ABUSIVE", "Abusive or offensive"),
        ("COPYRIGHT", "Copyright violation"),
        ("SPAM", "Spam or irrelevant"),
        ("OTHER", "Other"),
    ])
    comment = models.TextField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'post')

class PostClick(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reaction")
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'post')

class PostSave(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reaction")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reaction")
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'post')

