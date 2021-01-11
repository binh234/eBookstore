var progressbar = document.getElementsByClassName("progressbar")
var steps = progressbar[0].children
var stt = document.getElementById("order_stt")
stt = stt.getAttribute("value")
if (stt > 3) {
    // stt = stt + 1
}
for (let i = 0; i <= stt && i < 5; i++) {
    steps[i].classList.add("active")
}


var submit_btn = document.getElementById("btn-update")
submit_btn.addEventListener("click", updateOrder)
var order_id = document.getElementById("order_id")
order_id = order_id.getAttribute("value")

function updateOrder() {
    console.log("update")
    if (stt == 1) {
        parent = submit_btn.parentNode
        parent.href = "/checkout/" + order_id
    } else if (stt + 1 > steps.length) {
        var url = "/order_update/"
        fetch(url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    'status': stt + 1,
                    'order': order_id
                })
            })
            .then((response) => response.json())
            .then((data) => {
                alert(data)
                window.location.reload()
            })
    } else {
        submit_btn.disabled = true
    }
}