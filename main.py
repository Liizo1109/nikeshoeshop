from flask import Flask, render_template, session, url_for, redirect, flash
from main_product import your_product  # Import blueprint sản phẩm
from main_cart import your_cart        # Import blueprint giỏ hàng
from main_login import your_login      # Import blueprint đăng nhập
from main_register import your_register # Import blueprint đăng ký
import sqlite3

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'      # Thiết lập secret key cho quản lý session và bảo mật
app.template_folder = "templates"       # Chỉ định thư mục cho các tệp HTML
app.static_folder = "static"            # Chỉ định thư mục cho các tệp tĩnh (CSS, JS)

# Đăng ký các blueprint để tạo các route theo mô-đun
app.register_blueprint(your_product)    # Đăng ký blueprint sản phẩm
app.register_blueprint(your_cart)       # Đăng ký blueprint giỏ hàng
app.register_blueprint(your_login)      # Đăng ký blueprint đăng nhập
app.register_blueprint(your_register)   # Đăng ký blueprint đăng ký

# Định nghĩa route trang chủ
@app.route('/')
def index():
    return render_template("index.html", search_text="")  # Trả về trang index.html với search_text rỗng

# Khởi chạy ứng dụng khi file được chạy trực tiếp
if __name__ == '__main__':
    app.run(debug=True)  # Chạy ứng dụng với chế độ debug bật
