from aiogram.dispatcher.filters.state import State, StatesGroup


class FiniteStatesMachine(StatesGroup):
    waiting_for_task_title = State()
    waiting_for_task_edit = State()
