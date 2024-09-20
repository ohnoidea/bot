from aiogram.utils.keyboard import ReplyKeyboardBuilder


def select_timezone():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Europe/Moscow')
    builder.button(text='Asia/Yekaterinburg')
    builder.button(text='UTC')
    builder.button(text='Get from location', request_location=True)

    builder.adjust(1, 1, 2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='+03')
