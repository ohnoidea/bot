import os

TG_API_TOKEN = os.getenv('MAGICIAN_BOT_TOKEN')

DB_CONNECTION_STRING = 'dbname=%s user=%s host=%s password=%s' % (
    os.getenv('MAGICIAN_BOT_DB_NAME'),
    os.getenv('MAGICIAN_BOT_DB_USER'),
    os.getenv('MAGICIAN_BOT_DB_HOST'),
    os.getenv('MAGICIAN_BOT_DB_PASSWORD'),
)

DB_URL = 'postgresql+psycopg2://%s:%s@l%s/%s' % (
    os.getenv('MAGICIAN_BOT_DB_USER'),
    os.getenv('MAGICIAN_BOT_DB_PASSWORD'),
    os.getenv('MAGICIAN_BOT_DB_HOST'),
    os.getenv('MAGICIAN_BOT_DB_NAME'),
)

admin_ids = [
    359667541,
]
