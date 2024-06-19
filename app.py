from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user, logout_user, login_required, login_user
import db as db_session
from users import User
import sqlite3

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = "Secret key"

'''
Прошлый код
'''
# @app.route('/profile', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         # проверка логина и пароля
#         return 'Вы вошли в систему!'
#     else:
#         return render_template('authorization.html')
#
#
#
# @app.route('/authorization', methods=['GET', 'POST'])
# def form_authorization():
#     if request.method == 'POST':
#         Login = request.form.get('Login')
#         Password = request.form.get('Password')
#
#         db_lp = sqlite3.connect('login_password.db')
#         cursor_db = db_lp.cursor()
#         cursor_db.execute(('''SELECT password FROM passwords
#                                                WHERE login = '{}';
#                                                ''').format(Login))
#         pas = cursor_db.fetchall()
#
#         cursor_db.close()
#         try:
#             if pas[0][0] != Password:
#                 return render_template('auth_bad.html')
#         except:
#             return render_template('auth_bad.html')
#
#         db_lp.close()
#         return render_template('profile.html')
#
#     return render_template('authorization.html')
#

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


# @app.route('/registration', methods=['GET', 'POST'])
# def form_registration():
#
#     if request.method == 'POST':
#
#         user = User(
#             name=request.form.get('name').data,
#             surname=request.form.get('last-name').data,
#             nickname=request.form.get('username').data,
#             password=request.form.get('password').data
#         )
#
#
#         session = db_session.create_session()
#         session.add(user)
#         session.commit()
#         return render_template('profile.html')
#
#     return render_template('registration.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Главная страница
    '''
    if current_user.is_authenticated:
        return render_template("index-in.html")
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Форма авторизации
    '''
    if request.method == 'POST':
        session = db_session.create_session()
        user = session.query(User).filter(User.nickname == request.form.get('username')).first()
        if str(user.password) == str(request.form.get('password')):
            login_user(user)
            return redirect(url_for('profile', nickname=user.nickname))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    '''
    Форма регистраци
    '''
    if request.method == 'POST':
        user = User(
            name=request.form.get('name'),
            surname=request.form.get('last-name'),
            nickname=request.form.get('username'),
            password=request.form.get('password')
        )

        session = db_session.create_session()
        session.add(user)
        session.commit()
        return redirect(url_for('profile', nickname=user.nickname))

    return render_template('registration.html')


@app.route('/profile/<string:nickname>', methods=['GET', 'POST'])
def profile(nickname):
    '''
    Страница профиля
    '''
    session = db_session.create_session()
    profile = session.query(User).filter(User.nickname == nickname).first()
    if current_user.is_authenticated:
        if request.method == "POST":
            if current_user == profile and request.form.get("about"):
                profile.about = request.form.get("about")
                session.commit()
        return render_template('profile-in.html', profile=profile, about_user=profile.about)
    return render_template('profile.html', profile=profile, about_user=profile.about)


@app.route('/search', methods=['GET', 'POST'])
def search():
    '''
    Страница поиска
    '''
    if current_user.is_authenticated:
        return render_template('search-in.html')
    return render_template('search.html')


@app.route('/post', methods=['GET', 'POST'])
def post():
    '''
    Страница поста
    '''
    if current_user.is_authenticated:
        return render_template('post-in.html')
    return render_template('post.html')


@app.route('/rating', methods=['GET', 'POST'])
def rating():
    '''
    Страница рейтинга
    '''
    if current_user.is_authenticated:
        return render_template('rating-in.html')
    return render_template('rating.html')


@app.route('/publication', methods=['GET', 'POST'])
def publication():
    '''
    Страница публикации
    '''
    if current_user.is_authenticated:
        return render_template('publication-in.html')
    return render_template('publication.html')

if __name__ == '__main__':
    db_session.global_init("login_password.db")
    app.run()

