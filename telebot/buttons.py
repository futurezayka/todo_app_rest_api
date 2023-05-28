from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

inline_button_list = InlineKeyboardButton('Список задач', callback_data='task_list')
inline_button_create = InlineKeyboardButton('Создать задачу', callback_data='create_task')

inline_keyboard = InlineKeyboardMarkup()

inline_keyboard.add(inline_button_list)
inline_keyboard.add(inline_button_create)
# inline_keyboard.add(inline_button_update)
# inline_keyboard.add(inline_button_delete)
