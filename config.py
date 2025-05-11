import os

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'gui12345'
    MYSQL_DB = 'academia'
    SECRET_KEY = os.urandom(24)
