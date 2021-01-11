var updateBtns = document.getElementsByClassName("update-cart")
var cartQuantity = document.getElementById("cart-quantity")
const itemQuantity = document.getElementById("book-quantity")

// book option change event
function updateBookOption(option) {
    if (option.value == "buy") {
        itemQuantity.disabled = false
    } else if (option.value == "eBuy") {
        itemQuantity.value = 1
        itemQuantity.disabled = true
    } else if (option.value == "eRent") {
        itemQuantity.disabled = false
    }
}

// add/remove/update item to cart
for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        if (user != "AnonymousUser") {
            var productId = this.dataset.product
            var action = this.dataset.action
            var quantity = 1
            var option;
            if (action == 'add') {
                quantity = itemQuantity.value
                option = document.querySelector('input[name="book-option"]:checked').value
            } else {
                option = this.dataset.option
            }

            console.log("product", productId, "action", action)
            console.log("User: ", user)
            console.log("quantity: ", quantity)
            console.log("option: ", option)

            updateUserOrder(productId, action, quantity, option)
        } else {
            alert("Please login to continue!")
        }
    })
}

function updateCart(item) {
    if (user != "AnonymousUser") {
        var productId = item.dataset.product
        var action = item.dataset.action
        var quantity = item.value
        var option = item.dataset.option

        console.log("product", productId, "action", action)
        console.log("User: ", user)
        console.log("quantity: ", quantity)
        console.log("option: ", option)

        updateUserOrder(productId, action, quantity, option)
    }
}

function updateUserOrder(productId, action, quantity, option) {
    console.log("The user is authenticated")

    var url = "/update-item/"

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action, 'quantity': quantity, 'option': option })
    })

    .then((response) => response.json())
        .then((data) => {
            let message = data.message
            let changed = data.changed
            console.log('data:', changed)
            if (message == "success") {
                if (action == "add") {
                    alert("Thêm vào giỏ hàng thành công")
                } else {
                    location.reload()
                }
            } else {
                alert(message)
                location.reload()
            }
            // location.reload()
        })
}