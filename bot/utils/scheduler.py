from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from datetime import datetime

from config import DB_URL
from utils.dbconnect import Request


class Scheduler:
    def __init__(self, bot: Bot, db_request: Request) -> None:
        self.bot = bot
        self.db_request = db_request
        self.scheduler = AsyncIOScheduler(timezone='UTC')
        self.scheduler.add_jobstore('sqlalchemy', url=DB_URL)

        self.scheduler.start()

    def _add_message(self, add_job_params: dict, job_id: int):
        self.scheduler.add_job(self.bot.send_message, **add_job_params, id=str(job_id), jobstore='sqlalchemy')

    async def add_all_messages(self):
        for id, user_id, add_job_params, message_text, status in await self.db_request.get_reminders():
            if status != 'Active':
                continue
            
            add_job_params |= {
                'kwargs': {'chat_id': user_id, 'text': message_text}
            }
            self._add_message(add_job_params, id)
    
    async def schedule_message_date(
            self, 
            user_id: int,
            message_text: str,
            date: datetime|str
    ) -> None:
        add_job_params = {
            'trigger': 'date',
            'run_date': str(date),
            'kwargs': {'chat_id': user_id, 'text': message_text}
        }
        id = await self.db_request.add_reminder(user_id, message_text, add_job_params)
        self._add_message(add_job_params, id)
    
    async def schedule_message_interval(
            self, 
            user_id, 
            message_text: str,
            start_date: datetime|str, 
            interval_days: int
    ) -> None:
        add_job_params = {
            'trigger': 'interval',
            'start_date': str(start_date),
            'days': interval_days,
            'kwargs': {'chat_id': user_id, 'text': message_text}
        }
        id = await self.db_request.add_reminder(user_id, message_text, add_job_params)
        self._add_message(add_job_params, id)
    
    async def schedule_message_cron(
            self,
            user_id: int,
            message_text: str,
            cron_args
    ) -> None:
        add_job_params = {
            'trigger': 'cron',
            'kwargs': {'chat_id': user_id, 'text': message_text},
            **cron_args
        }
        id = await self.db_request.add_reminder(user_id, message_text, add_job_params)
        self._add_message(add_job_params, id)

