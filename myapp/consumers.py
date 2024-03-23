import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatWindow, ChatMessage, Profile

User = get_user_model()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        user = self.scope['user']
        if user.is_authenticated:
            self.user = user
            await self.send({
                'type': 'websocket.accept'
            })

    async def websocket_receive(self, event):
        received_data = json.loads(event['text'])
        message = received_data.get('message')
        userchat_id = received_data.get('userchat_id')
        user_id = received_data.get('sender_id')

        if not message or not userchat_id or not user_id:
            print('Error:: Incomplete message data')
            return False

        sender = await self.get_user(user_id)
        userchat_obj = await self.get_userchat(userchat_id)

        if not sender:
            print('Error:: sent by user is incorrect')
        if not userchat_obj:
            print('Error:: UserChat id is incorrect')

        message_obj = await self.save_message(sender, message, userchat_obj)

    async def websocket_disconnect(self, event):
        pass

    @database_sync_to_async
    def get_userchat(self, userchat_id):
        return ChatWindow.objects.filter(id=userchat_id).first()

    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.filter(id=user_id).first()

    @database_sync_to_async
    def save_message(self, user, message, userchat):
        user_profile = Profile.objects.get(user=user)
        return ChatMessage.objects.create(user=user_profile, userchat=userchat, message=message)
