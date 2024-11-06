from flask import Flask, request, render_template, session, url_for, redirect, flash
from flask import Blueprint
import sqlite3

your_product:Flask = Flask(__name__)
your_product.secret_key = 'your_secret_key'
your_product.template_folder = "templates"
your_product.static_folder = "static"
your_login = Blueprint("your_login", __name__)

# Function to check if user exists in the database
def check_exists(username, password):
    result = False
    sqldbname = 'datanike/datanike.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    sqlcommand = "SELECT * FROM ADMIN WHERE username = ? AND password = ?"
    cursor.execute(sqlcommand, (username, password))
    data = cursor.fetchall()
    if len(data) > 0:
        result = True
    conn.close()
    return result

# Define the login route
@your_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_exists(username, password):
            session['username'] = username
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('index'))  # Redirect to home page
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng", "error")
    return render_template('login.html')
