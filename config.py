from dotenv import load_dotenv
import os

load_dotenv()
EMAIL_USUARIO = os.getenv("EMAIL_USUARIO")
SENHA_APP = os.getenv("SENHA_APP")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
