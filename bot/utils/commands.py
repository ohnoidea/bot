from aiogram import Bot
from aiogram.types import BotCommand

async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='help',
            description='What I can do'
        ),
        BotCommand(
            command='list',
            description='Show lists'
        ),
        BotCommand(
            command='reminder',
            description='Reminders'
        ),
        BotCommand(
            command='id',
            description='Get your telegram id'
        ),
        BotCommand(
            command='set_timezone',
            description='Set default timezone for you'
        ),
        BotCommand(
            command='cron_help',
            description='Cron instruction'
        )
    ]

    await bot.set_my_commands(commands)
