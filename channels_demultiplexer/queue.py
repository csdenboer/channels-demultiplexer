import asyncio

__all__ = ("MessageQueue",)


class MessageQueue(asyncio.Queue):
    """
    Queue for messages waiting to be processed by a consumer.
    """

    async def get(self):
        """
        Remove, mark done and return an item from the queue. If queue is empty, wait until an item is available.
        """
        item = await super().get()
        # mark done
        self.task_done()
        return item
