from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    friends=models.ManyToManyField("self", through='FriendsList', symmetrical=False)

class FriendsList(models.Model):
    user1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='responsers')
    user2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requesters')
    is_accepted = models.BooleanField(null=True, blank=True)

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sended_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    created_at = models.DateTimeField(auto_now_add=True)