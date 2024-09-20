from aiogram.utils.keyboard import ReplyKeyboardBuilder


def show_reminder_options():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Create')
    builder.button(text='Show')

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def show_repetition_types():
    builder = ReplyKeyboardBuilder()

    builder.button(text='Once')
    builder.button(text='Every X days')
    builder.button(text='Schedule')

    builder.adjust(1, repeat=True)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
