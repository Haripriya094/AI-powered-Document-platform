import os

from dotenv import load_dotenv
load_dotenv()

mongo_url=os.getenv('MONGO_URL')
mongo_db=os.getenv('MONGO_DB')
service_host=os.getenv('SERVICE_HOST')
port=os.getenv('PORT')