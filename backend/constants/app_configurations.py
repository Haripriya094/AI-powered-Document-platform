import os

from dotenv import load_dotenv
load_dotenv()

mongo_url=os.getenv('MONGO_URL')
mongo_db=os.getenv('MONGO_DB')
service_host=os.getenv('SERVICE_HOST')
port=os.getenv('PORT')
secrets = {
    "MODULE": "AI-Powered Resume Analyzer",
    "LOG-BASE-PATH": "logs/",
    "FILE-NAME": "AI-Powered Resume Analyzer.log",
    "LOG-HANDLERS": "console",
    "FILE-MAX-SIZE": "100",
    "FILE-BACKUP-COUNT": "5",
    "LOG-LEVEL": "DEBUG",
}

class LOG:
    MODULE = secrets["MODULE"]
    LOG_BASE_PATH = secrets["LOG-BASE-PATH"]
    FILE_NAME = os.path.join(LOG_BASE_PATH, secrets["FILE-NAME"])
    LOG_HANDLERS = secrets["LOG-HANDLERS"].split(',')
    FILE_MAX_SIZE = int(secrets["FILE-MAX-SIZE"])
    FILE_BACKUP_COUNT = int(secrets["FILE-BACKUP-COUNT"])
    LOG_LEVEL = secrets["LOG-LEVEL"]