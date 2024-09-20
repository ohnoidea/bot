from aiogram.filters.callback_data import CallbackData
from datetime import date

class CalendarData(CallbackData, prefix='calendar'):
    chosen_date: date | None
    from_date: date | None


class ListData(CallbackData, prefix='list'):
    user_id: int
    list_name: str
