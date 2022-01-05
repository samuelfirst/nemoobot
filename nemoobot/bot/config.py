import os
from dotenv import load_dotenv

project_folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(project_folder, '.env.dev'))

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

BOT_AUTH_TOKEN = os.getenv('BOT_AUTH_TOKEN')
BOT_NICKNAME = os.getenv('BOT_NICKNAME')

BASE_DRF_API_URL = os.getenv('BASE_API_URL', 'http://localhost:8000/api/v1/')

WS_HOST = os.getenv('WS_HOST')
WS_PORT = int(os.getenv('WS_PORT'))

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', 5672))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'guest')
RABBITMQ_BASE_EXCHANGE = os.getenv('RABBITMQ_BASE_EXCHANGE', 'messages')
RABBITMQ_BOT_QUEUE = os.getenv('RABBITMQ_BOT_QUEUE', 'command_to_bot')
RABBITMQ_BACKEND_QUEUE = os.getenv('RABBITMQ_BACKEND_QUEUE', 'command_from_bot')
