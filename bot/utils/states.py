from aiogram.fsm.state import StatesGroup, State


class BaseStates(StatesGroup):
    GET_TIMEZONE = State()


class ListStates(StatesGroup):
    GET_OPTION = State()
    GET_NAME = State()
    GET_KEY = State()
    GET_VALUE = State()


class ReminderStates(StatesGroup):
    GET_OPTION = State()
    GET_MESSAGE_TEXT = State()
    GET_REPETITION = State()

    GET_DATE = State()
    GET_TIME = State()

    INTERVAL_GET_DATE = State()
    GET_INTERVAL = State()
    INTERVAL_GET_TIME = State()

    CRON_GET_ARGS = State()
