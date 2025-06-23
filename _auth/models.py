from django.db import models
import uuid



class Auth(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True,null=False)
    password=models.TextField(null=True)
    isVerified=models.BooleanField(default=False)
    
    def __str__(self):
        return self.id+":"+self.email



