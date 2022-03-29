import os

from dotenv import load_dotenv
from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy import create_engine

load_dotenv()

HOST = os.getenv('host')
USERNAME = os.getenv('user')
PASSWORD = os.getenv('password')
DB_NAME = os.getenv('db_name')
PORT = os.getenv('port')


def create_engine_connection():
    db_engine = create_engine(
        f'postgresql+psycopg2:'
        f'//{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
    return db_engine


BaseClass = declarative_base()


class Groups(BaseClass):
    __tablename__ = 'Groups'

    group_id = Column(Integer, primary_key=True, autoincrement=False)
    group_name = Column(String(50), nullable=False)


class Users(BaseClass):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(250), nullable=False)
    chat_id = Column(Integer)
    group_id = Column(Integer, ForeignKey('Groups.group_id'))
    Group = relationship('Groups')


if __name__ == '__main__':
    db_engine = create_engine_connection()
    BaseClass.metadata.create_all(db_engine)