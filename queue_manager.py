import asyncio

video_queue = asyncio.Queue()

async def worker():
    while True:
        func, args = await video_queue.get()
        await func(*args)
        video_queue.task_done()