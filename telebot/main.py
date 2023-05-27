from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext

from telebot.API_KEY import API_TOKEN
from telebot.buttons import inline_keyboard
from telebot.commands import WELCOME_MESSAGE
from telebot.defines import get_task_list


bot = Bot(API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def welcome(message: types.Message):
    await message.reply(WELCOME_MESSAGE, reply_markup=inline_keyboard)


#
async def get_tasklist(callback_query: types.CallbackQuery):
    result = await get_task_list()
    if result:
        text_response = 'Ваши таски и их статус:\n\n'
        for data in result:
            text_response += f"Задача: '{data['title']}', Завершено: {data['completed']}\n"
        await bot.send_message(callback_query.from_user.id, text_response)
    else:
        await bot.send_message(callback_query.from_user.id, 'Задач еще нет!')


@dp.callback_query_handler(lambda c: c.data == 'task_list')
async def button_click_get_tasklist(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await get_tasklist(callback_query)


# @dp.message_handler()
# async def echo(message: types.Message):
#     pass
#
#
# @dp.message_handler()
# async def echo(message: types.Message):
#     pass


if __name__ == '__main__':
    executor.start_polling(dp)
