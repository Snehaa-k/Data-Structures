import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from urllib.parse import urlparse, parse_qs
import json
from .models import ChatMessages, Notification,CustomUser
from asgiref.sync import sync_to_async

class TravelChat(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get('query_string', b'').decode('utf-8')
        query_params = parse_qs(query_string)

        if query_params.get('receiver_id', [None])[0] == "null":
            self.room_group_name = None
        else:
            try:
                user_id = int(query_params.get('user_id', [None])[0])
                receiver_id = int(query_params.get('receiver_id', [None])[0])
                unread_count = await self.get_unread_messages_count(user_id)
                

                if user_id > receiver_id:
                    self.room_name = f'{user_id}_{receiver_id}'
                else:
                    self.room_name = f'{receiver_id}_{user_id}'

                self.room_group_name = 'chat_%s' % self.room_name

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()

                # Send a JSON message indicating successful connection
                await self.send(text_data=json.dumps({
                    'type': 'connection',
                    'room_group_name': self.room_group_name
                }))

                await self.send(text_data=json.dumps({
                    'type': 'unread_count',
                    'unread_count': unread_count
                            }))
            except (TypeError, IndexError):
                await self.close(code=4000)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        userId = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']
        sender_username = await self.get_username(userId)
        uread_count = await self.get_unread_messages_count(userId)

        
        await self.save_message(userId, receiver_id, message, self.room_group_name)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': userId,
                'receiver': receiver_id
            }
        )
        print('in chat')
        await self.channel_layer.group_send(
            f"notification_{receiver_id}",
            {
                'type' : 'send_notification',
                "data":{
                   'message':message,
                   'user':sender_username,
                   'unread_count':uread_count,
                   
                }
            }
        )
    

    async def chat_message(self, event):
        content = event['message']
        sender = event['sender']
        receiver = event['receiver']
        
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'content': content,
            'sender': sender,
            'receiver': receiver
        }))

    
       
        # if str(self.scope['user'].id) != str(sender):  # Notify only the receiver, not the sender
        #         await self.send(text_data=json.dumps({
        #             'type': 'notification',
        #             'content': f'New message from {sender}: {content}',
        #             'sender': sender,
        #             'receiver': receiver
        #         }))
    @database_sync_to_async
    def get_username(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            return user.username
        except CustomUser.DoesNotExist:
            return f"User {user_id}"
   
    @database_sync_to_async
    def get_unread_messages_count(self, user_id):
        return ChatMessages.objects.filter(receiver=user_id, is_read=False).count()
    
    

    @database_sync_to_async
    def mark_messages_as_read(self, user_id, room_group_name):
        ChatMessages.objects.filter(receiver=user_id, thread_name=room_group_name, is_read=False).update(is_read=True)
    

    @database_sync_to_async
    def save_message(self, sender, receiver, message,thread):
        
        try:
            sender = CustomUser.objects.get(id=sender)
            
        except CustomUser.DoesNotExist:
            print(f"Sender with ID {sender} does not exist")
          
        try:
            receiver = CustomUser.objects.get(id=receiver)
        except CustomUser.DoesNotExist:
            return
        ChatMessages.objects.create(sender = sender.id,receiver = receiver.id,content = message,thread_name= thread,is_read=False) 







class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_params = dict(parse_qs(self.scope['query_string'].decode()))
        try:
            user_id = int(query_params.get('user_id', [None])[0])
            self.room_name = f'{user_id}_room'
            self.room_group_name = f'notification_{user_id}'
       
        # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except (ValueError, TypeError) as e:
            await self.close(code=4000)
            self.room_group_name = None

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name') and self.room_group_name:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        else:
            print("No room group to disconnect from")

    async def send_notification(self, event):
        # notification = event['notification']
        # print(event,"haiiillllllllllllllllllllllllllllllllllllllllll")
        # timestamp = event.get('timestamp', None)  

        await self.send(text_data=json.dumps(event["data"]))

@database_sync_to_async
def create_notification(sender, receiver, notification_type, text, link=None):
   
    
    return Notification.objects.create(
        sender=sender,
        receiver=receiver,
        notification_type=notification_type,
        text=text,
        link=link,
        seen=False,
    )