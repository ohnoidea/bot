from aiogram import Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime
import pytz

from keyboards.calendar import inline_calendar
from keyboards.reminder import show_reminder_options, show_repetition_types
from utils.states import ReminderStates
from utils.dbconnect import Request
from utils.scheduler import Scheduler

from utils.functions import time_from_text

router = Router()


@router.message(Command('reminder'))
async def cmd_start(message: Message, state: FSMContext, db_request: Request):
    if not await db_request.has_timezone(message.from_user.id):
        return await message.answer('Timezone required, set with /set_timezone')
    await state.set_state(ReminderStates.GET_OPTION)
    return await message.answer('Choose reminder option', reply_markup=show_reminder_options())


@router.message(ReminderStates.GET_OPTION)
async def get_option_fsm(message: Message, bot: Bot, state: FSMContext):
    match message.text:
        case 'Show':
            pass

        case 'Create':
            await bot.delete_message(message.chat.id, message.message_id - 1)
            await state.set_state(ReminderStates.GET_MESSAGE_TEXT)
            return await message.answer('Enter message text:', reply_markup=ReplyKeyboardRemove())


@router.message(ReminderStates.GET_MESSAGE_TEXT)
async def create_reminder_get_message_text(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id - 1)

    if len(message.text) > 256:
        await state.clear()
        return await message.answer('Message text is too long', reply_markup=ReplyKeyboardRemove())
    await state.update_data(message_text=message.text)

    await state.set_state(ReminderStates.GET_REPETITION)
    return await message.answer('How do you want to be reminded?', reply_markup=show_repetition_types())


@router.message(ReminderStates.GET_REPETITION)
async def create_reminder_get_repetition(message: Message, bot: Bot, state: FSMContext, db_request: Request):
    await bot.delete_message(message.chat.id, message.message_id - 1)

    match message.text:
        case 'Once':
            await state.update_data(trigger='date')
            await state.set_state(ReminderStates.GET_DATE)
            return await message.answer('Enter date:', reply_markup=inline_calendar())

        case 'Every X days':
            await state.update_data(trigger='interval')
            await state.set_state(ReminderStates.INTERVAL_GET_DATE)
            return await message.answer('Enter starting date:', reply_markup=inline_calendar())

        case 'Schedule':
            await state.update_data(trigger='cron')
            await state.set_state(ReminderStates.CRON_GET_ARGS)
            return await message.answer('Enter cron args:\n<tg-spoiler>Use /cron_help if you are not sure</tg-spoiler>', reply_markup=ReplyKeyboardRemove())


@router.message(ReminderStates.GET_TIME)
async def create_reminder_get_time(message: Message, bot: Bot, state: FSMContext, db_request: Request, scheduler: Scheduler):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    data = await state.get_data()
    await state.clear()
    
    time = time_from_text(message.text)
    if not time:
        return await message.answer('Incorrect time')

    timezone_name = await db_request.get_timezone(message.from_user.id)
    timezone = pytz.timezone(timezone_name)
    try:
        dt = datetime.combine(data['date'], time)
    except:
        return await message.answer('Incorrect time')
    dt = timezone.normalize(timezone.localize(dt))

    await scheduler.schedule_message_date(
        message.from_user.id, 
        data['message_text'],
        dt.astimezone(pytz.utc)
    )

    return await message.answer(f'Reminder set to {dt.strftime('%H:%M %d-%m-%Y')}')


@router.message(ReminderStates.GET_INTERVAL)
async def create_reminder_get_interval(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    try:
        period_in_days = int(message.text)
    except:
        await state.clear()
        return await message.answer('Incorrect period')
    await state.update_data(period=period_in_days)
    await state.set_state(ReminderStates.INTERVAL_GET_TIME)
    return await message.answer('Enter time:')


@router.message(ReminderStates.INTERVAL_GET_TIME)
async def create_reminder_inerval_get_time(message: Message, bot: Bot, state: FSMContext, db_request: Request, scheduler: Scheduler):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    data = await state.get_data()
    await state.clear()

    time = time_from_text(message.text)
    if not time:
        return await message.answer('Incorrect time')

    timezone_name = await db_request.get_timezone(message.from_user.id)
    timezone = pytz.timezone(timezone_name)
    try:
        dt = datetime.combine(data['starting_date'], time)
    except:
        return await message.answer('Incorrect time')
    dt = timezone.normalize(timezone.localize(dt))
    
    await scheduler.schedule_message_interval(
        message.from_user.id,
        data['message_text'],
        dt,
        data['period']
    )

    return await message.answer(
        f'Reminder set to {dt.strftime('%H:%M')}\n'\
        f'for every {data['period']} day from {dt.strftime('%d-%m-%Y')}'
    )


@router.message(ReminderStates.CRON_GET_ARGS)
async def create_reminder_cron_get_args(message: Message, bot: Bot, state: FSMContext, scheduler: Scheduler):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    data = await state.get_data()
    await state.clear()

    
    cron_args = dict(
        [keyval.split('=') for keyval in message.text.split()]
    )

    await scheduler.schedule_message_cron(
        message.from_user.id,
        data['message_text'],
        cron_args
    )

    return await message.answer('Reminder has been set')
