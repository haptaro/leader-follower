import asyncio
from collections import defaultdict

class SimplePubSub:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def publish(self, topic, message):
        for queue in self.subscribers[topic]:
            queue.put_nowait(message)

    async def subscribe(self, topic):
        queue = asyncio.Queue()
        self.subscribers[topic].append(queue)
        try:
            while True:
                message = await queue.get()
                yield message
        finally:
            self.subscribers[topic].remove(queue)

pubsub = SimplePubSub()
