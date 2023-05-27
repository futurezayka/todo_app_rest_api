from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

inline_button_list = InlineKeyboardButton('Task list', callback_data='task_list')
inline_button_create = InlineKeyboardButton('Create task', callback_data='create_task')
# inline_button_update = InlineKeyboardButton('Update task', callback_data='update_task')
# inline_button_delete = InlineKeyboardButton('Delete task', callback_data='delete_task')

inline_keyboard = InlineKeyboardMarkup()

inline_keyboard.add(inline_button_list)
inline_keyboard.add(inline_button_create)
# inline_keyboard.add(inline_button_update)
# inline_keyboard.add(inline_button_delete)

