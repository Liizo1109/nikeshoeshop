from flask import Flask, request, render_template, session, url_for, redirect, jsonify
from flask import Blueprint
import sqlite3

# Khởi tạo ứng dụng Flask và cấu hình cho Blueprint sản phẩm
your_product: Flask = Flask(__name__)
your_product.secret_key = 'your_secret_key'  # Thiết lập secret key để quản lý session
your_product.template_folder = "templates"  # Chỉ định thư mục cho các tệp HTML
your_product.static_folder = "static"  # Chỉ định thư mục cho các tệp tĩnh
your_product = Blueprint("your_product", __name__)  # Tạo blueprint cho chức năng quản lý sản phẩm


# Route tìm kiếm sản phẩm trong cơ sở dữ liệu
@your_product.route("/search", methods=['GET', 'POST'])
def load_data_from_db(search_text=""):
    sqldbname = 'datanike/datanike.db'  # Đường dẫn tới cơ sở dữ liệu SQLite
    if search_text != "":  # Kiểm tra nếu có từ khóa tìm kiếm
        conn = sqlite3.connect(sqldbname)  # Kết nối tới cơ sở dữ liệu
        cursor = conn.cursor()  # Tạo con trỏ để thực hiện truy vấn
        # Câu lệnh SQL tìm kiếm theo từ khóa trong tên sản phẩm, thương hiệu, hoặc chi tiết sản phẩm
        sqlcommand = ("SELECT * FROM nike "
                      "WHERE product LIKE '%" + search_text + "%'")
        sqlcommand += " OR brand LIKE '%" + search_text + "%'"
        sqlcommand += " OR details LIKE '%" + search_text + "%'"

        cursor.execute(sqlcommand)  # Thực hiện câu truy vấn
        data = cursor.fetchall()  # Lấy tất cả kết quả tìm kiếm
        conn.close()  # Đóng kết nối cơ sở dữ liệu
        return data  # Trả về danh sách kết quả tìm kiếm


# Route xử lý tìm kiếm và hiển thị kết quả
@your_product.route("/searchData", methods=['GET', 'POST'])
def searchData():
    if 'searchInput' in request.form:  # Kiểm tra nếu form có chứa 'searchInput'
        search_text = request.form['searchInput']  # Lấy giá trị từ form tìm kiếm
        html_table = load_data_from_db(search_text=search_text)  # Lấy kết quả từ hàm tìm kiếm
        print(html_table)  # In kết quả ra để kiểm tra
        # Hiển thị trang kết quả tìm kiếm với từ khóa và bảng kết quả
        return render_template('search.html',
                               search_text=search_text,
                               table=html_table)


# Route thêm sản phẩm vào giỏ hàng
@your_product.route("/cart/add", methods=['GET', 'POST'])
def add_to_cart():
    # 1. Khai báo tên Database để lấy thông tin sản phẩm
    sqldbname = 'datanike/datanike.db'
    # 2. Lấy ID sản phẩm và số lượng từ form
    product_id = request.form["product_id"]
    quantity = int(request.form.get("quantity"))

    # 3. Lấy tên và giá sản phẩm từ cơ sở dữ liệu
    with sqlite3.connect(sqldbname) as connection:  # Kết nối tới cơ sở dữ liệu
        cursor = connection.cursor()
        cursor.execute("SELECT product, price, picture, details "
                       "FROM nike WHERE id = ?",
                       (product_id,))  # Truy vấn để lấy thông tin sản phẩm theo ID
        product = cursor.fetchone()  # Lấy một sản phẩm từ kết quả truy vấn

    # 4. Tạo một từ điển chứa thông tin sản phẩm
    product_dict = {
        "id": product_id,
        "name": product[0],
        "price": product[1],
        "quantity": quantity,
        "picture": product[2],
        "details": product[3]
    }

    # 5. Lấy giỏ hàng từ session hoặc tạo danh sách rỗng nếu chưa có giỏ hàng
    cart = session.get("cart", [])

    # 6. Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    found = False
    for item in cart:
        if item["id"] == product_id:
            # 6.1 Nếu sản phẩm đã tồn tại trong giỏ hàng, cập nhật số lượng
            item["quantity"] += quantity
            found = True
            break
    if not found:
        # 6.2 Nếu sản phẩm chưa có trong giỏ hàng, thêm vào giỏ hàng
        cart.append(product_dict)

    # 7. Cập nhật giỏ hàng trong session
    session["cart"] = cart

    # 8. Trả về phản hồi JSON thông báo thêm sản phẩm thành công và số lượng sản phẩm trong giỏ
    return jsonify({"message": "Đã thêm sản phẩm vào giỏ hàng thành công!", "cart_count": len(cart)})
