from sqlalchemy import create_engine
from urllib.parse import quote_plus

def create_connection():
    username = 'supreme'
    password = quote_plus('@up3au42k7au4a83')
    hostname = 'ccu-rfid-project.mysql.database.azure.com'
    database = 'ccu-rfid-db'

    # 建立連線字串
    connection_string = f"mysql+mysqlconnector://{username}:{password}@{hostname}/{database}"

    # 建立引擎
    engine = create_engine(connection_string)
    return engine

engine = create_connection()
