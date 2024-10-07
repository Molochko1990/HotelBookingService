import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.DATABASE_URL = os.getenv('DATABASE_URL')

def get_config():
    return Config()
