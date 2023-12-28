from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class ActivePeriod(models.Model):
    id = models.IntegerField().primary_key
    label = models.CharField(max_length=250)
    seconds = models.IntegerField()


class Group(models.Model):
    id = models.UUIDField().primary_key
    owner = models.ForeignKey(User, related_name='group_owner', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    active_period = models.ForeignKey(ActivePeriod, on_delete=models.CASCADE)
    created_at = models.IntegerField()
    members = models.ManyToManyField(User)
