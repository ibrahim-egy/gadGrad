from flask import Flask, render_template, request, url_for, redirect
from detect import detect
from database import register_user, add_history
from numpy import asarray
from PIL import Image

app = Flask(__name__)
app.secret_key = "This is a secret"
EMAIL = "ibrahim@gmail.com"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result', methods=["GET", "POST"])
def result():
    if request.method == "POST":
        image = request.files.get('image')
        image.save(f"static/upload/{image.filename}")
        # img = Image.open(f"static/upload/{image.filename}")

        res = detect(f"static/upload/{image.filename}")
        # image_array = asarray(img)

        # add_history(EMAIL, image_array, res)

        return render_template('result.html', result=res)
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
