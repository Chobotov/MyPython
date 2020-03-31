from flask import Flask, render_template, Response
from flask_login import login_required,login_user,logout_user,LoginManager,UserMixin

from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from models import Dict, User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = '432532525_key'

NUM_USER = 0
Users=[]

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired])
    password = PasswordField('Password', validators=[DataRequired])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')

@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route('/')
@app.route('/index/')
@login_required
def index():
    username = "User"
    title = "Home Page"
    a = render_template('index.html', title = title, username = username)
    return a

@app.route('/main/')
@login_required
def main():
   result = ""
   for u in Users:
       result += u.get_info()

@app.route("/login",methods = ['GET','POST'])
def login():
    global NUM_USER
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User(NUM_USER)
        user.set_info(username,password)
        Users.append(user)
        logout_user(user)
        NUM_USER += 1
        return redirect("/main/")
    else:
        logout_user()
        render_template("login.html",form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p >')

if __name__ == '__main__':
    app.run()
