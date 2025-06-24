from django.db import models,IntegrityError
import uuid
import random 
import string
from django.utils import timezone


class IndustryType(models.TextChoices):
    TECH = "TECH", "Technology"
    FINANCE = "FIN", "Finance"
    EDUCATION = "EDU", "Education"
    HEALTHCARE = "HEALTH", "Healthcare"
    OTHER = "OTHER", "Other"

class User(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True,null=False)
    username=models.TextField(null=False,unique=True)
    auth=models.OneToOneField("_auth.Auth", related_name='user_account',on_delete=models.CASCADE,blank=False,null=False)
    description = models.TextField(blank=True, null=True)
    industryType = models.CharField(
        max_length=10,
        choices=IndustryType.choices,
        default=IndustryType.OTHER
    )
    profilePic=models.URLField(null=True,blank=True,default=None)
    DOB=models.DateField(null=True,blank=True)
    
    flagCount = models.PositiveIntegerField(default=0)
    isBanned = models.BooleanField(default=False)

    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    bannedAt = models.DateTimeField(auto_now=True)


    def generate_username(self, base_username):
        username = base_username
        while User.objects.filter(username=username).exists():
            suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            username = f"{base_username}_{suffix}"
        return username

    def save(self, *args, **kwargs):
        if not self.username:
            base_username = self.email.split("@")[0]
            self.username = self.generate_username(base_username)

        if self.flag_count >= 2 and not self.is_banned:
            self.is_banned = True
            self.flag_count = 0  
            self.banned_at = timezone.now()
            # notify via email/FCM here

        super().save(*args, **kwargs)






