from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import date, timedelta

from utils.callbackdata import CalendarData


def inline_calendar(from_date=date.today()):
    builder = InlineKeyboardBuilder()

    from_day = from_date.replace(day=1)
    to_day = (from_day + timedelta(days=32)).replace(day=1)

    builder.button(
        text='⬅️',
        callback_data=CalendarData(chosen_date=None, from_date=from_day-timedelta(days=1))
    )
    builder.button(text=from_date.strftime('%b %Y'), callback_data='None')
    builder.button(
        text='➡️',
        callback_data=CalendarData(chosen_date=None, from_date=to_day)
    )

    month_builder = InlineKeyboardBuilder()

    day = from_day - timedelta(days=from_day.weekday())
    while day < to_day:
        for _ in range(7):
            month_builder.button(
                text=str(day.day),
                callback_data=CalendarData(chosen_date=day, from_date=None)
            )
            day += timedelta(days=1)

    month_builder.adjust(7, repeat=True)
    builder.attach(month_builder)

    return builder.as_markup()
