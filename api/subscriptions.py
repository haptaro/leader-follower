import strawberry
from .pubsub import pubsub
from api.types import MessageType


@strawberry.type
class Subscription:
    
    # Subscription to receive messages sent in a specific chat room
    @strawberry.subscription
    async def message_sent(self, chat_room_id: int) -> MessageType:
        async for message in pubsub.subscribe(f"chat_{chat_room_id}"):
            yield message
