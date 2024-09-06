from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import MetaData, exc, select, update, exists
import sqlalchemy
import asyncio
import logging

from contextlib import asynccontextmanager
from db.models import *

engine = create_async_engine("mysql+aiomysql://root:615243qp@localhost:3306/site", future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
metadata = MetaData()
dialect = sqlalchemy.dialects.mysql.dialect()
logging.getLogger('sqlalchemy').setLevel(logging.getLevelName(30))

@asynccontextmanager
async def session_scope():
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

class Users:
    def __init__(self):
        pass

    async def add_user(self, username: str, password: str):  # Добавить пользователя в базу данных
        logging.info((username, password))
        try:
            async with session_scope() as s:
                s.add(UsersTable(username=username, password=password))
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка добавления пользователя", e)
            return None

    async def get_user_id(self, username):  # Проверить если ли пользователь в базе данных
        logging.info(username)
        try:
            async with session_scope() as s:
                check = await s.execute(select(UsersTable.id).where(UsersTable.username == "admin"))
                return check.scalar()
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка получения данных пользователя", e)
            return None

    async def check_user_exists(self, username):  # Проверить если ли пользователь в базе данных
        logging.info(username)
        try:
            async with session_scope() as s:
                check = await s.execute(select(exists().where(UsersTable.username == username)))
                return check.scalar()
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка проверки существования пользователя", e)
            return None

    async def check_user_password(self, username, password):  # Проверить если ли пользователь в базе данных
        logging.info((username, password))
        try:
            async with session_scope() as s:
                check = await s.execute(select(UsersTable.password).where(UsersTable.username == username))
                return check.scalar() == password
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка проверки пароля пользователя", e)
            return None

class Miners:
    def __init__(self):
        pass

    async def add_miner(
            self, id: str,
            computername: str = None,
            username: str = None,
            gpu: str = None,
            cpu: str = None,
            runtime: int = None,
            hashrate: dict = None):  # Добавить майнер в базу данных
        logging.info((id, computername, username, gpu, cpu, runtime, hashrate))
        try:
            async with session_scope() as s:
                s.add(MinersTable(id=id, computername=computername, username=username, gpu=gpu, cpu=cpu, runtime=runtime, hashrate=hashrate))
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка добавления майнера в базу данных", e)
            return None

    async def update_miner(
            self, id: str,
            computername: str = None,
            username: str = None,
            gpu: str = None,
            cpu: str = None,
            runtime: int = None,
            hashrate: dict = None):  # Обновить данные майнера в базе данных
        logging.info((id, computername, username, gpu, cpu, runtime, hashrate))
        try:
            async with session_scope() as s:
                await s.execute(update(MinersTable).where(MinersTable.id == id).values(computername=computername, username=username, gpu=gpu, cpu=cpu, runtime=runtime, hashrate=MinersTable.c.hashrate + hashrate))
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка обновления майнера базе данных", e)
            return None

async def main_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    miners_db = Miners()
    users_db = Users()
    print(await users_db.get_user_date("admin"))

if __name__ == '__main__':
    asyncio.run(main_db())