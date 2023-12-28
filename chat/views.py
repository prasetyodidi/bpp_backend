import time

from django.contrib.auth.models import User
from chat.models import Group, ActivePeriod
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def create_user_and_group(request):
    username = request.data['username']
    group_name = request.data['group_name']
    password = get_random_string(length=6)

    user = User.objects.create_user(username=username)
    user.set_password(password)
    user.save()

    active_period = ActivePeriod.objects.first()
    # group = Group.objects.create(name=group_name, owner_id=user, active_period=active_period, created_at=time.time())
    group = Group.objects.create(name=group_name, active_period=active_period, created_at=time.time())
    group.save()

    group.members.add(user)

    return Response({'account': {'username': username, 'password': password}, 'group': {'name': group.name}})


@api_view(['POST'])
def create_chat(request):
    text = request.data['text']
    group_id = request.data['groupId']
    
    group = get_object_or_404(Group, id=group_id)
    
    return Response({'message': 'Hello World!'})
