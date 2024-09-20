from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from timezonefinder import TimezoneFinder

from keyboards.base import select_timezone
from utils.states import BaseStates
from utils.dbconnect import Request

router = Router()
tf = TimezoneFinder()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Hello there\n<tg-spoiler>Ask master to add you</tg-spoiler>')


@router.message(Command('help'))
async def cmd_help(message: Message):
    help_message = \
        'What I can:\n'\
        '<b>Lists</b> - creates list of key-value pairs <tg-spoiler>(or key only)</tg-spoiler>\n'\
        '<b>Reminder</b> - sends message at given time <tg-spoiler>(use /set_timezone and check /cron_help for advanced setup)</tg-spoiler>\n'\
        
    await message.answer(help_message)


@router.message(Command('id'))
async def cmd_id(message: Message):
    await message.answer(f'Your id is <code>{message.from_user.id}</code>')


@router.message(Command('set_timezone'))
async def cmd_set_timezone(message: Message, state: FSMContext):
    await state.set_state(BaseStates.GET_TIMEZONE)
    return await message.answer(f'Select your time zone or enter it (like "+03")', reply_markup=select_timezone())


@router.message(Command('cron_help'))
async def cmd_cron_help(message: Message):
    return await message.answer(
        '<b>Example:</b> <code>day_of_week=fri hour=10-18 minute=*/15</code> for every 15 minutes between 10:00 and 18:00 on fridays\n'
        'Format <b>is important</b>. Use spaces only between arguments!!!\n\n'
        '<code>year       </code> - 4-digit year\n'
        '<code>month      </code> - month (1-12)\n'
        '<code>day        </code> - day of month (1-31)\n'
        '<code>week       </code> - ISO week (1-53)\n'
        '<code>day_of_week</code> - number or name of weekday (0-6 or mon, tue, wed, thu, fri, sat, sun)\n'
        '<code>hour       </code> - hour (0-23)\n'
        '<code>minute     </code> - minute (0-59)\n'
        '<code>second     </code> - second (0-59)\n\n'
        '<b>*:</b>\n'
        'Fire on every value\n'
        '<b>*/a:</b>\n'
        'Fire every a values, starting from the minimum\n'
        '<b>a-b:</b>\n'
        'Fire on any value within the a-b range (a must be smaller than b)\n'
        '<b>a-b/c:</b>\n'
        'Fire every c values within the a-b range\n'
        '<b>xth y (day only):</b>\n'
        'Fire on the x-th occurrence of weekday y within the month\n'
        '<b>last x (day only):</b>\n'
        'Fire on the last occurrence of weekday x within the month\n'
        '<b>last (day only):</b>\n'
        'Fire on the last day within the month\n'
        '<b>x, y, z:</b>\n'
        'Fire on any matching expression; can combine any number of any of the above expressions\n'
    )


@router.message(BaseStates.GET_TIMEZONE)
async def get_timezone(message: Message, state: FSMContext, db_request: Request):
    await state.clear()

    if message.location:
        timezone = tf.timezone_at(lng=message.location.longitude, lat=message.location.latitude)
    elif message.text in tf.timezone_names:
        timezone = message.text
    else:
        return await message.answer('No such timezone')
    
    await db_request.set_timezone(message.from_user.id, timezone)
    return await message.answer(f'Timezone set to {timezone}')
