from sqlalchemy import create_engine
from sqlalchemy.sql import text

# Create engine with the correct database URL
engine = create_engine("mysql+pymysql://root:615243qp@localhost:3306")

# Create a new database using the engine
with engine.connect() as connection:
    connection.execute(text("CREATE DATABASE site"))