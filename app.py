from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import hashlib
import os
from werkzeug.utils import secure_filename

from db.CRUD import Users, Miners

app = Flask(__name__)
app.secret_key = 'lalalalala'  # Замените на ваш секретный ключ

users_db = Users()
miners_db = Miners()



@app.route('/endpoint', methods=['GET', 'POST'])
async def endpoint():
    print('Endpoint', request.json)
    return 'Done'

@app.route('/endpoint.php', methods=['GET', 'POST'])
async def endpoint_php():
    print('Endpoint.php', request.json)
    return 'Done'



@app.route('/')
async def home():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    if 'user_id' in session:
        return redirect(url_for('admin_panel_main'))



@app.route('/admin_login', methods=['GET', 'POST'])
async def admin_login():
    if 'user_id' in session:
        return redirect(url_for('admin_panel_main'))

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()


        if await users_db.check_user_password(username, hashed_password):
            session['user_id'] = await users_db.get_user_id(username)
            return redirect(url_for('admin_panel_main'))

        else:
            error = 'Неправильное имя пользователя или пароль'

    return render_template('login_adm.html', error=error)



@app.route('/logout')
async def logout():
    # Удаление данных пользователя из сессии
    session.clear()
    # Перенаправление на главную страницу или страницу входа
    return redirect(url_for('admin_login'))



@app.route('/panel/main')
async def admin_panel_main():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin_panel.html', statistics=True)



@app.route('/panel/settings')
async def admin_panel_settings():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    return render_template('admin_panel.html', settings=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
