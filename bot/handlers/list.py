from aiogram import Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from keyboards.list import show_lists_keyboard, set_to_none_button
from utils.states import ListStates
from utils.dbconnect import Request

router = Router()


@router.message(Command('list'))
async def cmd_list(message: Message, db_request: Request):
    user_id = message.from_user.id

    lists = await db_request.get_lists(user_id)

    await message.answer('Your lists:', reply_markup=show_lists_keyboard(user_id, lists)) 


@router.message(ListStates.GET_OPTION)
async def get_option_fsm(message: Message, bot: Bot, state: FSMContext, db_request: Request):    
    await bot.delete_message(message.chat.id, message.message_id - 1)
    data = await state.get_data()
    
    match message.text:
        case 'Show':
            content = await db_request.list_get(data['user_id'], data['list_name'])
            text = ''
            for item, descr in content:
                line = item
                if descr:
                    line += f': {descr}'
                text += (line + '\n')
            if text == '':
                text = 'This list is empty'
            await state.clear()
            return await message.answer(text, reply_markup=ReplyKeyboardRemove())

        case 'Add record':
            await state.set_state(ListStates.GET_KEY)
            return await message.answer('Enter item:', reply_markup=ReplyKeyboardRemove())

        case 'Get random record':
            res = await db_request.list_get_random(data['user_id'], data['list_name'])
            await state.clear()
            
            if not res:
                return await message.answer('This list is empty')
            item, descr = res
            
            
            line = item
            if descr:
                line += f': {descr}'
            return await message.answer(line, reply_markup=ReplyKeyboardRemove())

        case 'Delete':
            await state.clear()
            await db_request.list_delete(data['user_id'], data['list_name'])
            return await message.answer('List has been deleted', reply_markup=ReplyKeyboardRemove())

    return await message.answer('No such option', reply_markup=ReplyKeyboardRemove())


@router.message(ListStates.GET_KEY)
async def get_list_item_fsm(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id - 1)

    item = message.text
    if len(item) > 64:
        await state.clear()
        return await message.answer('Item name is too long')

    await state.update_data(item=item)
    await state.set_state(ListStates.GET_VALUE)
    return await message.answer('Enter descriptoin:', reply_markup=set_to_none_button())


@router.message(ListStates.GET_VALUE)
async def get_list_item_descr_fsm(message: Message, bot: Bot, state: FSMContext, db_request: Request):
    await bot.delete_message(message.chat.id, message.message_id - 1)
    
    descr = message.text
    if len(descr) > 256:
        await state.clear()
        return await message.answer('Item name is too long', reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    await state.clear()
    await db_request.list_write(data['user_id'], data['list_name'], data['item'], descr)
    return await message.answer('Item added', reply_markup=ReplyKeyboardRemove())


@router.message(ListStates.GET_NAME)
async def create_list_fsm(message: Message, state: FSMContext, db_request: Request):
    await state.clear()
    list_name = message.text
    if len(list_name) > 64:
        return await message.answer('List name is too long')

    await db_request.add_list(message.from_user.id, list_name)
    return await message.answer(f'List {list_name} has been added')
