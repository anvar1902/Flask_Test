import sqlite3

# Создание или подключение к базе данных
conn = sqlite3.connect('database.db')

# Создание курсора
c = conn.cursor()

# Создание таблицы Users
c.execute('''CREATE TABLE IF NOT EXISTS users (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT,
             password TEXT)''')

# Закрытие соединения с базой данных
conn.close()
