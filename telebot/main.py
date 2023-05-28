from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from telebot.API_KEY import API_TOKEN
from telebot.FSM import FiniteStatesMachine
from telebot.buttons import inline_keyboard
from telebot.commands import WELCOME_MESSAGE
from telebot.defines import get_task_list, get_detail_info, delete_task, create_task, update_task

bot = Bot(API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    await message.reply(WELCOME_MESSAGE, reply_markup=inline_keyboard)


#
@dp.callback_query_handler(lambda callback_query: callback_query.data == 'task_list')
async def get_tasklist(callback_query: types.CallbackQuery):
    tasks = await get_task_list()
    if tasks:
        keyboard = types.InlineKeyboardMarkup()
        for task in tasks:
            button = types.InlineKeyboardButton(
                text=task['title'],
                callback_data=f'task_{task["id"]}'
            )
            keyboard.add(button)
        await bot.send_message(callback_query.from_user.id, '♥Выберите вашу задачу:', reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, 'Задач еще нет!')


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('task_'))
async def pick_the_task(callback_query: types.CallbackQuery):
    task_id = callback_query.data.split('_')[1]
    task = await get_detail_info(task_id)
    if task:
        text_response = f"Задача: '{task['title']}'"
        keyboard = types.InlineKeyboardMarkup()
        button_update = types.InlineKeyboardButton(text="Обновить задачу", callback_data=f'update_{task["id"]}')
        button_delete = types.InlineKeyboardButton(text="Удалить задачу", callback_data=f'delete_{task["id"]}')
        keyboard.add(button_update, button_delete)
        await bot.send_message(callback_query.from_user.id, text_response, reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, 'Задача не найдена.')


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('delete_'))
async def delete_the_task(callback_query: types.CallbackQuery):
    task_id = callback_query.data.split('_')[1]
    response_status = await delete_task(task_id)
    if response_status == 200:
        await bot.send_message(callback_query.from_user.id, 'Задача успешно удалена☺', reply_markup=inline_keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, 'Произошла ошибка (')


#

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'create_task')
async def create_handler(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Введите название задачи:')
    await FiniteStatesMachine.waiting_for_task_title.set()


@dp.message_handler(state=FiniteStatesMachine.waiting_for_task_title)
async def handle_task_title(message: types.Message, state: FSMContext):
    task_title = message.text
    data = {
        'title': task_title,
        'completed': False,
    }
    response_status = await create_task(data)
    if response_status == 200:
        await bot.send_message(message.chat.id, f'Вы создали задачу с названием: {task_title}',
                               reply_markup=inline_keyboard)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Произошла ошибка при создании задачи',
                               reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('update_'))
async def delete_the_task(callback_query: types.CallbackQuery, state: FSMContext):
    task_id = callback_query.data.split('_')[1]
    task = await get_detail_info(task_id)
    if task:
        edit_message_text = f"Текущая задача: '{task['title']}'\n"
        edit_message_text += "Введите новое название задачи:"
        await state.update_data(task_id=task_id)
        await FiniteStatesMachine.waiting_for_task_edit.set()
        await bot.edit_message_text(edit_message_text, chat_id=callback_query.from_user.id,
                                    message_id=callback_query.message.message_id)
    else:
        await bot.send_message(callback_query.from_user.id, 'Задача не найдена.')


@dp.message_handler(state=FiniteStatesMachine.waiting_for_task_edit)
async def handle_task_edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_id = data.get('task_id')
    new_task_title = message.text
    data = {
        'title': new_task_title,
    }
    status = await update_task(data, task_id)
    if status == 200:
        await bot.send_message(message.chat.id, "Задача успешно обновлена!",
                               reply_markup=inline_keyboard)
    else:
        await bot.send_message(message.chat.id, "Ошибка при обновлении задачи.")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
