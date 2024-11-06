from flask import Flask, request, render_template, session, url_for, redirect, flash
from flask import Blueprint
import sqlite3

# Tạo blueprint cho đăng ký
your_register = Blueprint("your_register", __name__)


# Hàm kiểm tra nếu tên đăng nhập đã tồn tại
def check_username_exists(username):
    sqldbname = 'datanike/datanike.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ADMIN WHERE username = ?", (username,))
    data = cursor.fetchall()
    conn.close()
    return len(data) > 0


# Hàm kiểm tra nếu email đã tồn tại
def check_email_exists(email):
    sqldbname = 'datanike/datanike.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ADMIN WHERE email = ?", (email,))
    data = cursor.fetchall()
    conn.close()
    return len(data) > 0


# Hàm thêm người dùng mới vào cơ sở dữ liệu
def add_user(username, email, password):
    sqldbname = 'datanike/datanike.db'
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ADMIN (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()


# Định nghĩa route cho đăng ký
@your_register.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Kiểm tra nếu tên đăng nhập đã tồn tại
        if check_username_exists(username):
            flash("Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.", "error")
        # Kiểm tra nếu email đã tồn tại
        elif check_email_exists(email):
            flash("Email này đã được sử dụng. Vui lòng nhập email khác.", "error")
        else:
            # Thêm người dùng vào cơ sở dữ liệu
            add_user(username, email, password)
            flash("Bạn đã đăng ký thành công, vui lòng đăng nhập lại.", "success")
            return redirect(url_for('your_login.login'))  # Chuyển hướng đến trang đăng nhập

    return render_template('register.html')
