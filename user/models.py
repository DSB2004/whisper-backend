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
    MEDIA = "MEDIA", "Media & Communication"
    GOVERNMENT = "GOV", "Government"
    RETAIL = "RETAIL", "Retail & E-commerce"
    MANUFACTURING = "MFG", "Manufacturing"
    LAW = "LAW", "Legal"
    CONSULTING = "CONSULT", "Consulting"
    NON_PROFIT = "NGO", "Non-profit"
    OTHER = "OTHER", "Other"



class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    NON_BINARY = "NB", "Non-binary"
    OTHER = "O", "Other"
    PREFER_NOT_TO_SAY = "NA", "Prefer not to say"

class EthnicGroup(models.TextChoices):
    ASIAN = "ASIAN", "Asian"
    BLACK = "BLACK", "Black or African descent"
    HISPANIC = "HISP", "Hispanic or Latino"
    WHITE = "WHITE", "White or Caucasian"
    MIDDLE_EASTERN = "ME", "Middle Eastern"
    NATIVE = "NATIVE", "Indigenous or Native"
    MIXED = "MIXED", "Mixed"
    OTHER = "OTHER", "Other"
    PREFER_NOT_TO_SAY = "NA", "Prefer not to say"



class User(models.Model): 
    from posts.models import TopicType
    # general info 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True,null=False)
    username=models.TextField(null=False,unique=True)
    auth=models.OneToOneField("_auth.Auth", related_name='user_account',on_delete=models.CASCADE,blank=False,null=False)
    description = models.TextField(blank=True, null=True)
    bio=models.TextField(null=True,blank=True)
    profilePic=models.URLField(null=True,blank=True,default=None)
    DOB=models.DateField(null=True,blank=True)
    gender = models.CharField(
    max_length=5,
    choices=Gender.choices,
    blank=True,
    null=True
    )


    # for demographics
    ethnicGroup = models.CharField(
        max_length=10,
        choices=EthnicGroup.choices,
        blank=True,
        null=True
    )
    country = models.CharField(max_length=100, blank=True, null=True)


    # preferences   
    preferredIndustry = models.ManyToManyField(
    max_length=10,
    choices=IndustryType.choices,
    default=IndustryType.OTHER
    )

    preferredTopics = models.ManyToManyField(TopicType, related_name='interested_users', blank=True)

    preferredLanguage = models.CharField(max_length=10, default="en")

    # status check
    flagCount = models.PositiveIntegerField(default=0)
    isBanned = models.BooleanField(default=False)


    bannedAt = models.DateTimeField(null=True, blank=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    lastActiveAt = models.DateTimeField(auto_now=True)

    def generateUsername(self, base_username):
        username = base_username
        while User.objects.filter(username=username).exists():
            suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            username = f"{base_username}_{suffix}"
        return username

    def save(self, *args, **kwargs):
        if not self.username:
            baseUsername = self.email.split("@")[0]
            self.username = self.generateUsername(baseUsername)

        if self.flagCount >= 2 and not self.isBanned:
            self.isBanned = True
            self.flagCount = 0  
            self.bannedAt= timezone.now()
            # notify via email/FCM here

        super().save(*args, **kwargs)






