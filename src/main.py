import os
from flask import Flask, render_template, request, url_for, redirect, session, flash
from detect import detect
from database import register_user, add_history, get_history, login_user
from flask_session import Session
import glob

app = Flask(__name__)
app.secret_key = "This is a secret"
# Creating Session Configs
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
EMAIL = "ibrahim@gmail.com"


@app.route('/')
def home():
    print(session.get('email'))
    print(session.get('logged_in'))
    print(session.get('username'))
    return render_template('index.html', logged_in=session.get('logged_in'))


@app.route('/instructions')
def instructions():
    return render_template('instructions.html', logged_in=session.get('logged_in'))


@app.route('/history')
def history():
    his = get_history(session.get('email'))
    return render_template('history.html', history=his, logged_in=session.get('logged_in'))


@app.route('/result', methods=["GET", "POST"])
def result():
    if request.method == "POST":
        image = request.files.get('uploadImage')

        path = f"static/upload/{image.filename}"
        image.save(path)

        res = detect(path)

        if session.get('logged_in'):
            add_history(session.get('email'), path, res)

        os.remove(path)

        return {
            'result': res
        }
    return render_template('result.html', result="", logged_in=session.get('logged_in'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')

        register_user(first_name, last_name, email, password, gender)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Email: {email}\nPassword: {password}")
        new_user = login_user(email, password)
        if new_user:
            session['email'] = email
            session['logged_in'] = True
            session['username'] = new_user[1]
            flash(f"Welcome Back {session.get('username')}")
            return redirect(url_for('home'))
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('email', None)
    session.pop('username', None)
    session['logged_in'] = False

    # Clear history folder
    for file in os.listdir('static/history'):
        os.remove(f"static/history/{file}")
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
