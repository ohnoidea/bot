from aiogram import types, Router, Bot
from aiogram.filters.command import Command
from middlewares.access import AdminMiddleware

router = Router()
router.message.middleware(AdminMiddleware())


@router.message(Command('test'))
async def cmd_test(message: types.Message):
    await message.answer('test')


@router.message(Command('add_user'))
async def cmd_add_user(message: types.Message, bot: Bot, **kwargs):
    try:
        user_id = int(kwargs['command'].args)
    except:
        return await message.answer('Wrong id')

    try:
        user = (await bot.get_chat_member(user_id, user_id)).user
    except:
        return await message.answer('No such user')
    
    request = kwargs['db_request']

    if await request.known_user(user_id):
        return await message.reply(f'{user.first_name} is already added')
    
    await request.add_user(user_id)
    await bot.send_message(user_id, '<i>Let the Force be with you<i>')
    return await message.reply(f'{user.first_name} (@{user.username}) added')
