from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login_check', methods=['POST'])
def login_check():

    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password)
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        role = result[0]

        if role == 'admin':
            return redirect('/admin')

        else:
            return redirect('/user')

    return "Invalid Username or Password"

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/user')
def user():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True)
