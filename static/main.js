// Hàm xóa ghi chú (nếu cần thiết)
function deleteNote(noteId) {
    // Gửi yêu cầu xóa ghi chú tới server qua phương thức POST
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),    // Gửi ID của ghi chú dưới dạng JSON
        headers: {
            "Content-Type": "application/json"       // Thiết lập Content-Type là JSON
        }
    }).then((_res) => {
        // Sau khi xóa thành công, tải lại trang để cập nhật giao diện
        window.location.href = "/";
    });
}

// Hàm thêm sản phẩm vào giỏ hàng bằng AJAX
function addToCart(productId) {
    // Lấy số lượng sản phẩm từ input (nếu không nhập số lượng thì mặc định là 1)
    const quantity = document.getElementById("quantity-" + productId).value || 1;

    // Gửi yêu cầu thêm sản phẩm vào giỏ hàng qua phương thức POST
    fetch("/cart/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"  // Thiết lập Content-Type cho form
        },
        // Dữ liệu gửi đi bao gồm ID sản phẩm và số lượng
        body: new URLSearchParams({
            product_id: productId,
            quantity: quantity
        })
    })
    .then((response) => response.json())                     // Chuyển đổi phản hồi từ server sang JSON
    .then((data) => {
        // Hiển thị thông báo khi thêm sản phẩm thành công
        alert(data.message);

        // Cập nhật số lượng sản phẩm trong giỏ hàng nếu có phần tử hiển thị
        const cartCount = document.getElementById("cart-count");
        if (cartCount) {
            cartCount.textContent = data.cart_count;         // Cập nhật số lượng sản phẩm trong giỏ hàng
        }
    })
    .catch((error) => {
        // Thông báo lỗi khi thêm sản phẩm thất bại
        console.error("Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng:", error);
        alert("Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng.");
    });
}

// Hiệu ứng "bouncing shoes" sử dụng thư viện anime.js
var bouncingShoes = anime({
    targets: '#shoe-target',               // Đặt hiệu ứng cho phần tử có ID là "shoe-target"
    translateY: '15',                      // Di chuyển phần tử lên xuống 15px
    duration: 2000,                        // Thời gian của một lần hiệu ứng là 2000ms
    loop: true,                            // Lặp lại hiệu ứng vô hạn
    direction: 'alternate',                // Đảo ngược hướng mỗi lần lặp (lên-xuống)
    easing: 'linear'                       // Thiết lập chuyển động mượt đều
});
