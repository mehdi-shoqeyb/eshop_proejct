import json
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import authenticate, login
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .serializers import MessageSerializer
from .models import Message,ChatRoom
from rest_framework.renderers import JSONRenderer
from account_module.models import User


class ChatConsumer(WebsocketConsumer):
    
    def new_message(self,data):
        text = data['message']
        athor = data['username']
        room_id = data['room_id']
        chatroom = ChatRoom.objects.get(room_id=room_id)
        user = User.objects.filter(username=athor).first()
        message = Message.objects.create(
            chatroom= chatroom,
            athor=user,
            text= text,
        )
        super_user = user.is_superuser
        result = eval(self.message_serializer(message))
        self.send_to_chat_message(result,super_user)
    
    
    def fetch_message(self,data):
        room_id = data['room_id']
        qs = Message.last_message(self,room_id)
        
        message_json = eval(self.message_serializer(qs=qs))

        for message in message_json:
            username = message['__str__']
            user = User.objects.filter(username=username).first()
            is_superuser = user.is_superuser
            message['is_superuser'] = is_superuser
        
        content = {
            'command':'fetch_message',
            'message':message_json[::-1],
        }
        
        self.chat_message(content)
    
    
    def message_serializer(self,qs):
        
        serialized = MessageSerializer(qs,many = (lambda qs : True if (qs.__class__.__name__ == 'QuerySet') else False)(qs))
        m_data = JSONRenderer().render(serialized.data)
        return m_data
    
    commands = {
        'new_message':new_message,
        'fetch_message':fetch_message
    }
    
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = (f'chat_{self.room_id}')
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()

    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
     
    def receive(self, text_data):
        text_data_dict = json.loads(text_data)

        command = text_data_dict['command']
        print(command)
        self.commands[command](self,text_data_dict)
        
        
        
    def send_to_chat_message(self,message,super_user):  
            async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                {  
                    'type': 'chat_message',
                    'command':'new_message',
                    'is_superuser':super_user,
                    'text':message['text'],
                    '__str__':message['__str__'],
                    'timestamp':message['timestamp'],
                }
            )
            
    def chat_message(self,event):
        self.send(text_data=json.dumps(event))
            