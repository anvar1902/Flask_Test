from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean, Float, text, JSON
import sqlalchemy
import datetime

Base = declarative_base()

class UsersTable(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(255), nullable=False, unique=True)
    password = Column('password', String(255), nullable=False)

class MinersTable(Base):
    __tablename__ = 'miners_data'
    id = Column('id', String(255), primary_key=True)
    computername = Column('computername', String(255))
    username = Column('username', String(255))
    gpu = Column('gpu', String(255))
    cpu = Column('cpu', String(255))
    runtime = Column('runtime', Integer)
    hashrate = Column('hashrate', JSON)
