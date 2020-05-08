import requests
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from requests import post, get

from blog_package import app, db
from blog_package.models import Message, User

key = "f057e20c89f41d00710591d8ecba6988"
s_city = "Tambov,RU"
city_id = 0


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/main', methods=['GET'])
@login_required
def main():
    city_id = get_city_id(s_city)
    data = request_current_weather(city_id)
    conditions = data['weather'][0]['description']
    temp = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    return render_template('main.html', conditions=conditions, temp=temp, temp_min=temp_min, temp_max=temp_max,
                           messages=Message.query.all())


@app.route('/add_message', methods=['POST'])
@login_required
def add_message():
    text = request.form['text']
    tag = request.form['tag']
    db.session.add(Message(text, tag))
    db.session.commit()

    return redirect(url_for('main'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста, заполните поля ввода!')
        elif password != password2:
            flash('Пароли не похожи!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('main'))
        else:
            flash('Неверный логин/пароль')
    else:
        flash('Пожалуйста! Введите логин/пароль')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)
    return response


def get_city_id(s_city_name):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': key})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        # print("city:", cities)
        city_id = data['list'][0]['id']
        # print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        pass
    assert isinstance(city_id, int)
    return city_id


# Запрос текущей погоды
def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': key})
        data = res.json()
        # print("conditions:", data['weather'][0]['description'])
        # print("temp:", data['main']['temp'])
        # print("temp_min:", data['main']['temp_min'])
        # print("temp_max:", data['main']['temp_max'])
        # print("data:", data)
    except Exception as e:
        print("Exception (weather):", e)
        pass
    return data
