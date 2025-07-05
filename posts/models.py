from django.db import models
import uuid
from user.models import User

class AssetsType(models.TextChoices):
    IMG = "IMG", "Images"
    AUDIO = "AUDIO", "Audio"
    VIDEO = "VIDEO", "Video"
    OTHER ="OTHER",'Other'

class TopicType(models.TextChoices):
    WORKPLACE = "WORK", "Workplace Experiences"
    MENTAL_HEALTH = "MENTAL", "Mental Health"
    PRODUCTIVITY = "PROD", "Productivity"
    TECH_TRENDS = "TECH", "Tech & Trends"
    CAREER_ADVICE = "CAREER", "Career Advice"
    REMOTE_WORK = "REMOTE", "Remote Work"
    STARTUPS = "STARTUP", "Startups"
    OFFICE_POLITICS = "POLITICS", "Office Politics"
    SALARIES = "SALARY", "Salaries & Compensation"
    DIVERSITY = "DIVERSITY", "Diversity & Inclusion"
    INTERVIEWS = "INTERVIEW", "Interviews & Hiring"
    RELATIONSHIPS = "RELATION", "Workplace Relationships"
    PERSONAL_STORIES = "STORY", "Personal Stories"
    CONFESSIONS = "CONFESS", "Confessions"
    LEADERSHIP = "LEAD", "Leadership & Management"
    FREELANCING = "FREELANCE", "Freelancing"
    SIDE_HUSTLES = "SIDE", "Side Hustles"
    EDUCATION = "EDU", "Learning & Education"
    NEWS = "NEWS", "Industry News"
    GENERAL = "GEN", "General Discussion"


class Post(models.Model): 
    from user.models import User
    from community.models import Community
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title=models.TextField(blank=False,null=False)
    body=models.TextField(blank=False,null=False)
    community = models.ForeignKey(
        Community,
        related_name="community_related_post",
        on_delete=models.SET_NULL,  
        null=True,
        blank=True
    )
    
    isVerified=models.BooleanField(default=False)
    isHidden=models.BooleanField(default=False)
    
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)



class PostTopics:
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post=models.ForeignKey(Post,related_name="community_related_topics",on_delete=models.CASCADE)
    topic=models.CharField(
        max_length=10,
        choices=TopicType.choices,
        blank=True,
        null=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)


class PostAssets(models.Model):
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



