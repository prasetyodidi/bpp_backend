import time

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from chat.models import Group, ActivePeriod, Message
from rest_framework.response import Response
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404

from chat.mqtt import client as mqtt_client
import json
from django.utils import timezone


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

@api_view(['POST'])
def create_user_and_group(request):
    username = request.data['username']
    group_name = request.data['groupName']
    password = get_random_string(length=6)

    user = User.objects.create_user(username=username, password=password)
    user.save()

    active_period = ActivePeriod.objects.first()
    group_code = get_random_string(6)
    group = Group.objects.create(
        name=group_name,
        owner=user,
        active_period=active_period,
        created_at=int(time.time()),
        code=group_code
    )

    group.save()

    group.members.add(user)

    return Response({
        "account": {
            "username": username,
            "password": password
        },
        "group": {
            "name": group_name,
            "code": group_code
        }
    })
    

@api_view(['POST'])
def create_user_and_join_group(request):
    username = request.data['username']
    group_code = request.data['groupCode']
    password = get_random_string(length=6)

    user = User.objects.create_user(username=username, password=password)
    user.save()
    
    group = get_object_or_404(Group.objects.filter(code=group_code))
    group.members.add(user)
    
    web_response = {
        'account': {
            'name': user.username,
            'password': password,
        },
        'group': {
            'id': group.id,
            'name': group.name,
        }
    }

    return Response(web_response)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_groups(request):
    user = request.user

    data = GroupSerializer(Group.objects.filter(members__id=user.id), many=True).data
    return Response(data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def messages_by_group_id(request, group_id):
    group = get_object_or_404(Group.objects.filter(id=group_id))  
    
    messages = Message.objects.prefetch_related('owner').filter(group_id=group_id)
    
    data_messages = []
    for message in messages:
        data_messages.append({
            "id": message.id,
            "message": message.message,
            "group": 21,
            "createdAt": message.created_at.strftime("%H:%M"),
            'owner': {
                'username': message.owner.username,
            }
        })

    data = GroupSerializer(group, many=False).data
    messages_data = MessageSerializer(messages, many=True).data
    return Response(data_messages)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def join_group(request):
    group_code = request.data['group_code']

    user = request.user

    group = get_object_or_404(Group.objects.filter(code=group_code))
    group.members.add(user)

    groups_data = GroupSerializer(Group.objects.filter(members__id=user.id), many=True).data
    return Response({'groups': groups_data})


@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_message(request):
    text = request.data['text']
    group_id = request.data['groupId']

    user = request.user
    group = get_object_or_404(Group.objects.filter(id=group_id))

    message = Message.objects.create(message=text, owner=user, group=group, created_at=timezone.now() + timezone.timedelta(hours=7))
    message.save()
    
    mqtt_message = {
        "key": message.id,
        "msg": text,
        "username": user.username,
        "createdAt": message.created_at.strftime("%H:%M"),
    }
    
    json_message = json.dumps(mqtt_message)
    
    topic = "group/" + group.code
    
    msg_count = 1
    
    while True:
        time.sleep(1)
        result = mqtt_client.publish(topic, json_message)
        status = result[0]
        if status == 0:
            print(f"Send `{json_message}` to topic `{topic}`")
        else:
            print(f"Failed to send {json_message} to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break

    return Response({'message': text, 'topic': topic, 'result': result[0]})


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_time_period(request, group_id):
    active_period_id = request.data['activePeriodId']
    active_period = ActivePeriod.objects.filter(id=active_period_id).first()
    
    group = Group.objects.filter(id=group_id).first()
    group.active_period = active_period
    group.save()
    
    group_data = {
        'name': group.name,
        'activePeriodId': group.active_period.id
    }
    
    return Response({'message': 'changed ', 'groupId': group_id, 'group': group_data, 'activePeriodId': active_period_id})
