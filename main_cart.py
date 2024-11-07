from flask import Flask, request, render_template, session, url_for, redirect
from flask import Blueprint
import sqlite3

# Tạo ứng dụng Flask và thiết lập các cấu hình cơ bản
your_cart: Flask = Flask(__name__)
your_cart.secret_key = 'your_secret_key'  # Thiết lập secret key cho quản lý session
your_cart.template_folder = "templates"  # Chỉ định thư mục cho các tệp HTML
your_cart.static_folder = "static"  # Chỉ định thư mục cho các tệp tĩnh (CSS, JS)
your_cart = Blueprint("your_cart", __name__)  # Tạo blueprint cho chức năng giỏ hàng


# Định nghĩa route hiển thị giỏ hàng
@your_cart.route("/viewcart", methods=['GET', 'POST'])
def view_cart():
    current_cart = []  # Danh sách sản phẩm trong giỏ hàng hiện tại
    if 'cart' in session:  # Kiểm tra nếu có giỏ hàng trong session
        current_cart = session.get("cart", [])  # Lấy giỏ hàng từ session
    if 'current_username' in session:  # Kiểm tra nếu có thông tin người dùng trong session
        current_username = session['current_user']['name']  # Lấy tên người dùng từ session
    else:
        current_username = ""  # Nếu không có thông tin, để tên người dùng rỗng
    return render_template('viewcart.html', carts=current_cart, user_name=current_username)  # Trả về trang giỏ hàng


# Định nghĩa route cập nhật giỏ hàng
@your_cart.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', [])  # Lấy giỏ hàng từ session
    new_cart = []  # Tạo danh sách mới để lưu sản phẩm đã cập nhật
    for product in cart:  # Lặp qua từng sản phẩm trong giỏ hàng
        product_id = str(product['id'])  # Lấy ID của sản phẩm
        # Kiểm tra nếu có số lượng mới của sản phẩm trong form
        if f'quantity-{product_id}' in request.form:
            quantity = int(request.form[f'quantity-{product_id}'])
            # Nếu số lượng là 0 hoặc có yêu cầu xóa sản phẩm, bỏ qua sản phẩm này
            if quantity == 0 or f'delete-{product_id}' in request.form:
                continue
            product['quantity'] = quantity  # Cập nhật số lượng của sản phẩm
        new_cart.append(product)  # Thêm sản phẩm đã cập nhật vào danh sách mới
    session['cart'] = new_cart  # Cập nhật giỏ hàng trong session
    return redirect(url_for('your_cart.view_cart'))  # Chuyển hướng đến trang giỏ hàng sau khi cập nhật


# Định nghĩa route tiến hành đặt hàng
@your_cart.route("/proceed_cart", methods=['GET', 'POST'])
def proceed_cart():
    # Kiểm tra nếu có thông tin người dùng trong session
    if 'current_user' in session:
        user_id = session['current_user']['id']  # Lấy ID người dùng từ session
        user_email = session['current_user']['email']  # Lấy email người dùng từ session
    else:
        user_id = 0  # Nếu không có thông tin, đặt ID và email về 0
        user_email = 0

    # Lấy giỏ hàng từ session
    current_cart = []
    if 'cart' in session:
        shopping_cart = session.get("cart", [])  # Lấy giỏ hàng từ session

    # Lưu thông tin đơn hàng vào bảng "Order" trong cơ sở dữ liệu
    sqldbname = 'datanike/datanike.db'  # Đường dẫn tới cơ sở dữ liệu SQLite
    conn = sqlite3.connect(sqldbname)  # Kết nối tới cơ sở dữ liệu
    cursor = conn.cursor()  # Tạo con trỏ để thực hiện truy vấn

    # Định nghĩa thông tin đơn hàng (đặt mặc định cho ví dụ này)
    user_address = "User Address"  # Địa chỉ người dùng
    user_mobile = "User Mobile"  # Số điện thoại người dùng
    purchase_date = "2023-10-23"  # Ngày mua
    ship_date = "2023-10-25"  # Ngày giao hàng dự kiến
    status = 1  # Trạng thái đơn hàng (1: đang xử lý)

    # Chèn đơn hàng vào bảng "order"
    cursor.execute('''INSERT INTO "order" (user_id, user_email, 
                   user_address, user_mobile, purchase_date, 
                   ship_date, status) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (user_id, user_email, user_address, user_mobile, purchase_date, ship_date, status))

    # Lấy ID của đơn hàng vừa chèn
    order_id = cursor.lastrowid  # ID đơn hàng
    print(order_id)  # In ID đơn hàng (chỉ để kiểm tra)

    # Xác nhận và đóng kết nối cơ sở dữ liệu
    conn.commit()
    conn.close()

    # Lưu chi tiết đơn hàng vào bảng "order_details"
    conn = sqlite3.connect(sqldbname)  # Mở lại kết nối cơ sở dữ liệu
    cursor = conn.cursor()  # Tạo con trỏ để thực hiện truy vấn

    # Lặp qua từng sản phẩm trong giỏ hàng để lưu vào "order_details"
    for product in shopping_cart:
        product_id = product['id']  # ID sản phẩm
        price = product['price']  # Giá sản phẩm
        quantity = product['quantity']  # Số lượng sản phẩm

        # Chèn chi tiết sản phẩm vào bảng "order_details"
        cursor.execute('''INSERT INTO order_details 
                       (order_id, product_id, price, quantity) VALUES (?, ?, ?, ?) ''',
                       (order_id, product_id, price, quantity))

    # Xác nhận và đóng kết nối cơ sở dữ liệu
    conn.commit()
    conn.close()

    # Xóa giỏ hàng hiện tại khỏi session sau khi đặt hàng thành công
    if 'cart' in session:
        current_cart = session.pop("cart", [])  # Xóa giỏ hàng trong session
    else:
        print("No current_cart in session")  # In thông báo nếu không có giỏ hàng trong session

    # Tạo URL để chuyển hướng đến trang đơn hàng
    order_url = url_for('orders', user_id=user_id, _external=True)
    return f'Redirecting to order page: <a href ="{order_url}">{order_url}</a>'  # Hiển thị liên kết tới trang đơn hàng
