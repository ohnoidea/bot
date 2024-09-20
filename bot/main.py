import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging as log

import config
from utils.scheduler import Scheduler
from utils.commands import set_commands
from utils.dbconnect import create_connection_pool, Request

from middlewares.access     import AuthMiddleware
from middlewares.dbsession  import DBSessionMiddleware
from middlewares.scheduler  import SchedulerMiddleware

from handlers.admin     import router as admin_router
from handlers.base      import router as base_router
from handlers.list      import router as list_router
from handlers.reminder  import router as reminder_router
from handlers.callback  import router as callback_router


bot = Bot(
    token=config.TG_API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_routers(
    base_router,
    admin_router,
    list_router,
    reminder_router,
    callback_router
)


async def start_bot(bot: Bot):
    for admin_id in config.admin_ids:
        await bot.send_message(admin_id, '<b>Hello there</b>')


async def stop_bot(bot: Bot):
    for admin_id in config.admin_ids:
        await bot.send_message(admin_id, '<b>Bye</b> 👋')


async def start():
    connection_pool = await create_connection_pool(config.DB_CONNECTION_STRING)
    async with connection_pool.connection() as conn:
        scheduler = Scheduler(bot, Request(conn))
    await scheduler.add_all_messages()

    dp.update.middleware(DBSessionMiddleware(connection_pool))
    dp.update.middleware(AuthMiddleware())
    dp.update.middleware(SchedulerMiddleware(scheduler))

    await set_commands(bot)
 
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    log.basicConfig(
        level=log.INFO,
        filename='/var/log/magician/magician.log',
        format='%(asctime)s [%(levelname)s]: %(message)s'
    )

    try:
        asyncio.run(start())
    except Exception as e:
        log.error(str(e))
