from flask import Flask, request, render_template, session, url_for, redirect, flash
from flask import Blueprint
import sqlite3

# Khởi tạo ứng dụng Flask và thiết lập các cấu hình cơ bản
your_product:Flask = Flask(__name__)
your_product.secret_key = 'your_secret_key'       # Thiết lập secret key để quản lý session
your_product.template_folder = "templates"        # Chỉ định thư mục cho các tệp HTML
your_product.static_folder = "static"             # Chỉ định thư mục cho các tệp tĩnh (CSS, JS)
your_login = Blueprint("your_login", __name__)    # Tạo blueprint cho chức năng đăng nhập

# Hàm kiểm tra nếu người dùng tồn tại trong cơ sở dữ liệu
def check_exists(username, password):
    result = False                                # Biến kết quả mặc định là False (người dùng không tồn tại)
    sqldbname = 'datanike/datanike.db'            # Đường dẫn tới cơ sở dữ liệu SQLite
    conn = sqlite3.connect(sqldbname)             # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor()                        # Tạo con trỏ để thực hiện truy vấn
    sqlcommand = "SELECT * FROM ADMIN WHERE username = ? AND password = ?"  # Câu lệnh SQL để kiểm tra người dùng
    cursor.execute(sqlcommand, (username, password))  # Thực hiện câu truy vấn với tên đăng nhập và mật khẩu
    data = cursor.fetchall()                      # Lấy tất cả kết quả truy vấn
    if len(data) > 0:                             # Nếu có kết quả, người dùng tồn tại
        result = True                             # Đặt kết quả là True
    conn.close()                                  # Đóng kết nối cơ sở dữ liệu
    return result                                 # Trả về kết quả (True nếu người dùng tồn tại)

# Định nghĩa route cho trang đăng nhập
@your_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':                  # Kiểm tra nếu request là POST
        username = request.form['username']       # Lấy tên đăng nhập từ form
        password = request.form['password']       # Lấy mật khẩu từ form
        if check_exists(username, password):      # Kiểm tra nếu người dùng tồn tại
            session['username'] = username        # Lưu tên đăng nhập vào session
            flash("Đăng nhập thành công!", "success")  # Thông báo đăng nhập thành công
            return redirect(url_for('index'))     # Chuyển hướng đến trang chủ sau khi đăng nhập thành công
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng", "error")  # Thông báo lỗi nếu thông tin không chính xác
    return render_template('login.html')          # Hiển thị trang đăng nhập nếu request là GET hoặc đăng nhập thất bại
