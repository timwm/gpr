from django.db import models

from core.models.user import User


class ActiveSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
