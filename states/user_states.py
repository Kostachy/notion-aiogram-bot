from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    input_data = State()
