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
