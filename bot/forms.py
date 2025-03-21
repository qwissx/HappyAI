from aiogram.dispatcher.filters.state import State, StatesGroup

class FUser(StatesGroup):
    thread_id = State()
