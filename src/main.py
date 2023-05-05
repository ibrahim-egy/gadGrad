from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('email')
        password = request.form.get('password')
        print(f"Email: {username}\nPassword: {password}")

    return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')

        print(f"Name: {first_name} {last_name}\nEmail: {email}\nPassword: {password}\nGender: {gender}")
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
