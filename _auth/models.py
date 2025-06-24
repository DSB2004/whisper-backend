from django.db import models, IntegrityError,transaction
import uuid

class Auth(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email=models.EmailField(unique=True,null=False)
    password=models.TextField(null=True)
    isVerified=models.BooleanField(default=False)
    user=models.OneToOneField("user.User", related_name='user_profile', on_delete=models.SET_NULL, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id+":"+self.email

    def save(self, *args, **kwargs):
        if self.pk:
            old = Auth.objects.get(pk=self.pk)
            if not old.isVerified and self.isVerified:
                with transaction.atomic():
                    self.createUserAccount()
                
        super().save(*args, **kwargs)


    def createUserAccount(self):
        from  user.models import User
        try:
            self.user=User.objects.create(email=self.email)
        except IntegrityError:
            try:
                self.user=User.get(email=self.email)
            except User.DoesNotExist:
                pass


