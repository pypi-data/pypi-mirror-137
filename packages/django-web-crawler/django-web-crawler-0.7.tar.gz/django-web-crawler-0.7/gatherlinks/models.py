from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class LinkModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    links = models.CharField(max_length=500)
