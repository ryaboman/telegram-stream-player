from aiogram.fsm.state import StatesGroup, State

class StepsViewProjects(StatesGroup):
    TC_WAIT_TEXT = State()
    AR_WAIT_PHOTO = State()
    NR_WAIT_IMG = State()
    TA_WAIT_AUDIO = State()
