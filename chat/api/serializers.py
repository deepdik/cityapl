# from django.contrib.sessions.models import Session
from django.db.models import Q
from django.db.models import Count 

import datetime
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    
    )

from chat.models import (
    Dialog,
    Message
    )

from accounts.api.serializers import UserDetailSerializer
from django.conf import settings

class DialogListSerializer(ModelSerializer):
    owner= UserDetailSerializer(read_only=True)
    opponent= UserDetailSerializer(read_only=True)

    class Meta:
        model = Dialog
        fields = [
            'owner',
            'opponent',
            'id'                     
        ]

class MessageListSerializer(ModelSerializer):
    sender=UserDetailSerializer(read_only=True)
    opponent=UserDetailSerializer(read_only=True)
    # session_key = SerializerMethodField()

  

    # def get_session_key(self, obj):
    #     user = self.context['request'].user.pk
    #     session_key = self.context['request'].COOKIES[settings.SESSION_COOKIE_NAME]
       
    #     return session_key
   
    class Meta:
        model = Message
        fields = [
            'dialog',           
            'sender',
            'text',
            'seen',
            'opponent',
            'get_formatted_create_datetime',
            'id', 
               
        ]
class DialogNotificationSerializer(ModelSerializer):
    No_of_unseen_messages = SerializerMethodField()

    def get_No_of_unseen_messages(self, instance):
        user = self.context['request'].user
     
        No_of_unseen_messages = Message.objects.filter(Q(dialog = instance.id, receiver__username = user,seen = False)).count()
        print(No_of_unseen_messages )
        # data = MessageListSerializer(instance,many=True).data

        # print(data , "2222222")
        # return data
        return No_of_unseen_messages
        

    class Meta:
        model = Dialog
        fields=[
            'id',
            'No_of_unseen_messages'
            
                        
        ]

class DialogBlockSerializer(ModelSerializer):
    class Meta:
        model = Dialog
        fields=[
            'dialog_status_owner',
            'dialog_status_opponent'

        ]   
class DeleteMsgSerializer(ModelSerializer):
    
    class Meta:
        model = Message
        fields = [
            'id',
            'dialog'





        ]