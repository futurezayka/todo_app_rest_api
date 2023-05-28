from aiogram.dispatcher.filters.state import State, StatesGroup


class FiniteStatesMachine(StatesGroup):
    waiting_for_task_title = State()
