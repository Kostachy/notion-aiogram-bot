from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    input_data = State()
