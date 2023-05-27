import aiohttp
from aiogram.types import update


async def get_task_list():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/task-list') as response:
            data = await response.json()
            return data
