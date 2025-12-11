import json
# --- 1. Use the ASYNC consumer ---
from channels.generic.websocket import AsyncWebsocketConsumer
# --- 2. Import the database wrapper ---
from channels.db import database_sync_to_async

from django.contrib.auth import get_user_model

User = get_user_model()

# --- 3. Use the ASYNC class ---
class ChatConsumer(AsyncWebsocketConsumer):
    
    # --- 4. This is now ASYNC ---
    async def connect(self):
        # Get user IDs from the URL
        self.user_1_id = int(self.scope['url_route']['kwargs']['user_1_id'])
        self.user_2_id = int(self.scope['url_route']['kwargs']['user_2_id'])
        
        # --- 5. THE REAL FIX ---
        # We wrap our database validation in a helper
        is_allowed = await self.check_user_allowed()
        
        if not is_allowed:
            await self.close()
            return
        # --- END OF FIX ---

        # Sort the IDs to create a consistent room name
        if self.user_1_id < self.user_2_id:
            self.room_name = f'chat_{self.user_1_id}_{self.user_2_id}'
        else:
            self.room_name = f'chat_{self.user_2_id}_{self.user_1_id}'
            
        self.room_group_name = f'group_{self.room_name}'

        # Join room group (this is already async, no wrapper needed)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept the connection
        await self.accept()

    # --- 6. ADD THIS HELPER FUNCTION ---
    # This function safely runs our sync DB query in an async context
    @database_sync_to_async
    def check_user_allowed(self):
        # self.scope['user'] is a sync database call
        # By putting it here, we are telling Django
        # to run it safely in a separate thread.
        current_user_id = self.scope['user'].id
        if current_user_id not in [self.user_1_id, self.user_2_id]:
            return False
        return True
    # --- END OF HELPER ---

    # --- 7. disconnect, receive, and chat_message are all ASYNC ---
    async def disconnect(self, close_code):
        # Leave room group (already async)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (already async)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Get the sender's email to display
        # We must use our helper to access the user
        sender_email = await self.get_sender_email()

        # Send message to room group (already async)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_email': sender_email
            }
        )
        
    # --- 8. ADD THIS SECOND HELPER FUNCTION ---
    @database_sync_to_async
    def get_sender_email(self):
        return self.scope['user'].email
    # --- END OF HELPER ---

    # Receive message from room group (already async)
    async def chat_message(self, event):
        message = event['message']
        sender_email = event['sender_email']

        # Send message to WebSocket (already async)
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_email': sender_email
        }))