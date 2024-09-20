from aiogram import Router, F
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from keyboards.list import show_list_options
from keyboards.calendar import inline_calendar
import utils.callbackdata as callback
from utils.states import ListStates, ReminderStates

router = Router()


@router.callback_query(callback.ListData.filter())
async def list_data_callback(
        callback: CallbackQuery,
        callback_data: callback.ListData,
        state: FSMContext
) -> None:
    await state.set_state(ListStates.GET_OPTION)
    await state.update_data(
        user_id=callback_data.user_id,
        list_name=callback_data.list_name
    )
    await callback.message.answer(
        text=callback_data.list_name,
        reply_markup=show_list_options()
    )
    await callback.answer()


@router.callback_query(F.data == 'create_list')
async def create_list_callback(
    callback: CallbackQuery,
    state: FSMContext
) -> None:
    await state.set_state(ListStates.GET_NAME)
    await callback.message.answer(
        text='Enter new list name:',
        reply_markup=ReplyKeyboardRemove()
    )
    await callback.answer()


@router.callback_query(callback.CalendarData.filter(), ReminderStates.GET_DATE)
async def reminder_date_calendar_callback(
        callback: CallbackQuery,
        callback_data: callback.CalendarData,
        state: FSMContext
) -> None:
    if callback_data.chosen_date:
        await state.update_data(date=callback_data.chosen_date)
        await state.set_state(ReminderStates.GET_TIME)
        await callback.message.answer('Enter time:')
        await callback.message.delete()
    elif callback_data.from_date:
        await callback.message.edit_reply_markup(
            reply_markup=inline_calendar(callback_data.from_date)
        )


@router.callback_query(callback.CalendarData.filter(), ReminderStates.INTERVAL_GET_DATE)
async def reminder_interval_calendar_callback(
        callback: CallbackQuery,
        callback_data: callback.CalendarData,
        state: FSMContext
) -> None:
    if callback_data.chosen_date:
        await state.update_data(starting_date=callback_data.chosen_date)
        await state.set_state(ReminderStates.GET_INTERVAL)
        await callback.message.answer('Enter interval in days:')
        await callback.message.delete()
    elif callback_data.from_date:
        await callback.message.edit_reply_markup(
            reply_markup=inline_calendar(callback_data.from_date)
        )
