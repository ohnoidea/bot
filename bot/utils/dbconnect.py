import psycopg_pool
from psycopg.types.json import Jsonb


async def create_connection_pool(connection_strig: str):
    pool = psycopg_pool.AsyncConnectionPool(connection_strig, open=False)
    await pool.open()
    return pool


class Request:
    def __init__(self, connection: psycopg_pool.AsyncConnectionPool.connection):
        self.connection = connection


    async def add_user(self, user_id: int) -> None:
        query = 'INSERT INTO users (telegram_id) VALUES (%s);'
        await self.connection.execute(query, (user_id,))
        await self.connection.commit()


    async def known_user(self, user_id: int) -> bool:
        query = 'SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id=%s);'

        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            return (await cursor.fetchone())[0]


    async def has_timezone(self, user_id: int) -> bool:
        query = 'SELECT EXISTS(SELECT 1 FROM users WHERE telegram_id=%s AND timezone IS NOT NULL);'

        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            return (await cursor.fetchone())[0]


    async def set_timezone(self, user_id: int, timezone: str):
        query = "UPDATE users SET timezone=%s WHERE telegram_id=%s;"

        await self.connection.execute(query, (timezone, user_id))
        await self.connection.commit()


    async def get_timezone(self, user_id: int) -> str:
        query = 'SELECT timezone FROM users WHERE telegram_id=%s;'

        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            return (await cursor.fetchone())[0]

    ###############################################################################################

    async def get_lists(self, user_id: int):
        query = 'SELECT DISTINCT list_name FROM list WHERE user_id=%s;'

        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (user_id,))
            return [x[0] for x in (await cursor.fetchall())]


    async def add_list(self, user_id: int, list_name: str):
        query = "INSERT INTO list VALUES (%s, %s, NULL, NULL)"

        await self.connection.execute(query, (user_id, list_name))
        await self.connection.commit()

    ###############################################################################################

    async def list_get(self, user_id: int, list_name: str):
        query = """
            SELECT item, item_description 
            FROM list 
            WHERE user_id=%s AND list_name=%s AND item IS NOT NULL;"""

        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (user_id, list_name))
            return await cursor.fetchall()


    async def list_write(self, user_id: int, list_name: str, item: str, descr: str):
        query = 'INSERT INTO list VALUES (%s, %s, %s, %s);'

        if descr == 'None':
            descr = None

        await self.connection.execute(query, (user_id, list_name, item, descr))
        await self.connection.commit()


    async def list_get_random(self, user_id: int, list_name: str):
        query = """
            WITH cur_list AS (
                SELECT item, item_description
                FROM list
                WHERE user_id=%s AND list_name=%s AND item IS NOT NULL
            )
            SELECT *
            FROM cur_list
            OFFSET floor(random() * (SELECT COUNT(*) FROM cur_list))
            LIMIT 1;"""

        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (user_id, list_name))
            return await cursor.fetchone()


    async def list_delete(self, user_id: int, list_name: str):
        query = 'DELETE FROM list WHERE user_id=%s AND list_name=%s;'

        await self.connection.execute(query, (user_id, list_name))
        await self.connection.commit()

    ###############################################################################################

    async def add_reminder(self, user_id: int, message_text: str, add_job_kwargs: dict):
        query = "INSERT INTO reminder VALUES (DEFAULT, %s, %s, %s, 'Active') RETURNING id;"

        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (user_id, Jsonb(add_job_kwargs), message_text))
            await self.connection.commit()
            return (await cursor.fetchone())[0]


    async def get_reminders(self):
        query = 'SELECT * FROM reminder;'

        async with self.connection.cursor() as cursor:
            await cursor.execute(query)
            return await cursor.fetchall()
    

    async def remove_reminder(self, reminder_id: int):
        query = "UPDATE reminder SET status='Disabled' WHERE id = %d;"

        await self.connection.execute(query, (reminder_id,))
        await self.connection.commit()
