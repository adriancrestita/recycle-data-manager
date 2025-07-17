import psycopg2
import os
from dotenv import load_dotenv

# Cargar .env desde ./config/.env
load_dotenv(dotenv_path='./config/.env')

def get_connection():
    return psycopg2.connect(os.getenv("DB_URL"))
