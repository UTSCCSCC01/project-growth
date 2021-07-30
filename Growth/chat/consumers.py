# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope['path_remaining'])
        self.room_name = self.scope['path_remaining'][14:]
        self.room_name = self.room_name[:-1]
        self.room_group_name = 'video_chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print('Disconnected!')
        

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_json = json.loads(text_data)
        peer_username = text_json['peer']
        action = text_json['action']
        message = text_json['message']

        # print('unanswered_offers: ', self.unanswered_offers)

        print('Message received: ', message)

        print('peer_username: ', peer_username)
        print('action: ', action)
        print('self.channel_name: ', self.channel_name)

        if(action == 'new-offer') or (action =='new-answer'):
            # in case its a new offer or answer
            # send it to the new peer or initial offerer respectively

            receiver_channel_name = text_json['message']['receiver_channel_name']

            print('Sending to ', receiver_channel_name)

            # set new receiver as the current sender
            text_json['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'text_json': text_json,
                }
            )

            return

        # set new receiver as the current sender
        # so that some messages can be sent
        # to this channel specifically
        text_json['message']['receiver_channel_name'] = self.channel_name

        # send to all peers
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'text_json': text_json,
            }
        )

    async def send_sdp(self, event):
        text_json = event['text_json']
        print(text_json['peer'])
        this_peer = text_json['peer']
        action = text_json['action']
        message = text_json['message']

        await self.send(text_data=json.dumps({
            'peer': this_peer,
            'action': action,
            'message': message,
        }))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print('Room Group Name', self.room_group_name)
        print('Room Name:', self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))