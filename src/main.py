import os

from flask import Flask, render_template, request, url_for, redirect
from detect import detect
from database import register_user, add_history, get_history

app = Flask(__name__)
app.secret_key = "This is a secret"
# testing
EMAIL = "ibrahim@gmail.com"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/instructions')
def instructions():
    return render_template('instructions.html')


@app.route('/history')
def history():
    his = get_history(EMAIL)
    return render_template('history.html', history=his)


@app.route('/result', methods=["GET", "POST"])
def result():
    if request.method == "POST":
        image = request.files.get('uploadImage')

        path = f"static/upload/{image.filename}"
        image.save(path)

        res = detect(path)
        add_history(EMAIL, path, res)

        os.remove(path)

        return {
            'result': res
        }
    return render_template('result.html', result="")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')

        new_user = register_user(first_name, last_name, email, password, gender)
        EMAIL = new_user
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Email: {email}\nPassword: {password}")
        # login_user(email, password)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
