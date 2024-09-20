from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.callbackdata import ListData


def show_lists_keyboard(user_id: int, list_names: list[str]):
    builder = InlineKeyboardBuilder()

    for list_name in list_names:
        builder.button(text=list_name, callback_data=ListData(user_id=user_id, list_name=list_name))

    builder.button(text='✍️ Create a list', callback_data='create_list')

    builder.adjust(1, repeat=True)
    return builder.as_markup()


def show_list_options():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Show')
    builder.button(text='Add record')
    builder.button(text='Get random record')
    builder.button(text='Delete')

    builder.adjust(2, 1, 1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def set_to_none_button():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='None')]], resize_keyboard=True)
