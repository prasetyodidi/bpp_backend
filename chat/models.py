from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()


class ActivePeriod(models.Model):
    id = models.IntegerField().primary_key
    label = models.CharField(max_length=250)
    seconds = models.IntegerField()


class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=20, unique=True)
    active_period = models.ForeignKey(ActivePeriod, on_delete=models.CASCADE)
    created_at = models.IntegerField()
    members = models.ManyToManyField(User, related_name='members')


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(db_default=timezone.make_aware(timezone.datetime(2023, 1, 31, 13, 35)))

