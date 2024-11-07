from flask import Flask, request, render_template, session, url_for, redirect, flash
from flask import Blueprint
import sqlite3

# Tạo blueprint cho chức năng đăng ký
your_register = Blueprint("your_register", __name__)

# Hàm kiểm tra nếu tên đăng nhập đã tồn tại trong cơ sở dữ liệu
def check_username_exists(username):
    sqldbname = 'datanike/datanike.db'              # Đường dẫn tới cơ sở dữ liệu SQLite
    conn = sqlite3.connect(sqldbname)                # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor()                           # Tạo con trỏ để thực hiện truy vấn
    cursor.execute("SELECT * FROM ADMIN WHERE username = ?", (username,))  # Kiểm tra username
    data = cursor.fetchall()                         # Lấy tất cả kết quả trả về
    conn.close()                                     # Đóng kết nối cơ sở dữ liệu
    return len(data) > 0                             # Trả về True nếu username đã tồn tại

# Hàm kiểm tra nếu email đã tồn tại trong cơ sở dữ liệu
def check_email_exists(email):
    sqldbname = 'datanike/datanike.db'              # Đường dẫn tới cơ sở dữ liệu SQLite
    conn = sqlite3.connect(sqldbname)                # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor()                           # Tạo con trỏ để thực hiện truy vấn
    cursor.execute("SELECT * FROM ADMIN WHERE email = ?",
                   (email,))  # Kiểm tra email
    data = cursor.fetchall()                         # Lấy tất cả kết quả trả về
    conn.close()                                     # Đóng kết nối cơ sở dữ liệu
    return len(data) > 0                             # Trả về True nếu email đã tồn tại

# Hàm thêm người dùng mới vào cơ sở dữ liệu
def add_user(username, email, password):
    sqldbname = 'datanike/datanike.db'              # Đường dẫn tới cơ sở dữ liệu SQLite
    conn = sqlite3.connect(sqldbname)                # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor()                           # Tạo con trỏ để thực hiện truy vấn
    # Chèn thông tin người dùng mới vào bảng ADMIN
    cursor.execute("INSERT INTO ADMIN (username, email, password) VALUES (?, ?, ?)",
                   (username, email, password))
    conn.commit()                                    # Lưu thay đổi vào cơ sở dữ liệu
    conn.close()                                     # Đóng kết nối cơ sở dữ liệu

# Định nghĩa route cho trang đăng ký
@your_register.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':                     # Kiểm tra nếu request là POST
        username = request.form['username']          # Lấy tên đăng nhập từ form
        email = request.form['email']                # Lấy email từ form
        password = request.form['password']          # Lấy mật khẩu từ form

        # Kiểm tra nếu tên đăng nhập đã tồn tại
        if check_username_exists(username):
            flash("Tên đăng nhập đã tồn tại. Vui lòng chọn tên khác.", "error")  # Thông báo lỗi nếu tên đã tồn tại
        # Kiểm tra nếu email đã tồn tại
        elif check_email_exists(email):
            flash("Email này đã được sử dụng. Vui lòng nhập email khác.", "error")  # Thông báo lỗi nếu email đã tồn tại
        else:
            # Thêm người dùng mới vào cơ sở dữ liệu
            add_user(username, email, password)
            flash("Bạn đã đăng ký thành công, vui lòng đăng nhập lại.", "success")  # Thông báo thành công
            return redirect(url_for('your_login.login'))  # Chuyển hướng đến trang đăng nhập

    return render_template('register.html')          # Hiển thị form đăng ký nếu request là GET hoặc đăng ký không thành công
