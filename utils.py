from pymongo import MongoClient
from dotenv import load_dotenv
import os

db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
mongo_client_string = os.getenv('MONGO_CLIENT')

def get_db_handle(db_name, host, port, user_name, password):
    client = MongoClient(host=host, port=port, user_name=user_name, password=password )
    db_handle = client[db_name]
    return client, db_handle
    # client = MongoClient(host='localhost', db_name='fp_customer_db', port=27017, )

client = MongoClient(mongo_client_string)