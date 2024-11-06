// Hàm xóa ghi chú (nếu cần thiết)
function deleteNote(noteId) {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then((_res) => {
        window.location.href = "/";
    });
}

// Hàm thêm sản phẩm vào giỏ hàng bằng AJAX
function addToCart(productId) {
    // Lấy số lượng sản phẩm từ input
    const quantity = document.getElementById("quantity-" + productId).value || 1;

    fetch("/cart/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            product_id: productId,
            quantity: quantity
        })
    })
    .then((response) => response.json())
    .then((data) => {
        // Hiển thị thông báo thêm thành công
        alert(data.message);

        // Cập nhật số lượng sản phẩm trong giỏ hàng nếu có phần tử hiển thị
        const cartCount = document.getElementById("cart-count");
        if (cartCount) {
            cartCount.textContent = data.cart_count;
        }
    })
    .catch((error) => {
        console.error("Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng:", error);
        alert("Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng.");
    });
}

// Hiệu ứng "bouncing shoes"
var bouncingShoes = anime({
    targets: '#shoe-target',
    translateY: '15',
    duration: 2000,
    loop: true,
    direction: 'alternate',
    easing: 'linear'
});
