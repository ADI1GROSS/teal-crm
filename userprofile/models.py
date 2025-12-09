from django.contrib.auth.models import User
from django.db import models
import uuid 

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    invite_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    fields = models.JSONField(default=dict, blank=True)
    name = models.CharField(verbose_name="שם", max_length=100, blank=True, null=True)
    email = models.EmailField(verbose_name="אימייל", default='')
    phone = models.CharField(verbose_name="טלפון", max_length=50, default='')
    regulations_document = models.FileField(upload_to='regulations/',blank=True, null=True)


    def __str__(self):
        return self.user.username
    

    