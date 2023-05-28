import aiohttp
from aiogram.types import update


async def get_task_list():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/api/task-list') as response:
            data = await response.json()
            return data


async def get_detail_info(task_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://127.0.0.1:8000/api/task-detail/{task_id}') as response:
            data = await response.json()
            return data


async def delete_task(task_id):
    async with aiohttp.ClientSession() as session:
        async with session.delete(f'http://127.0.0.1:8000/api/task-delete/{task_id}') as response:
            return response.status


async def create_task(data):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://127.0.0.1:8000/api/task-create/", json=data) as response:
            return response.status


async def update_task(data, task_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8000/api/task-update/{task_id}", json=data) as response:
            return response.status
