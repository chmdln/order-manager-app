const mainMenuButtonSidebar = document.querySelector(".js-main-menu-button-sidebar")
mainMenuButtonSidebar.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com'
})


document.addEventListener("DOMContentLoaded", function () {
    const statusElements = document.querySelectorAll(".curr-order-status");

    statusElements.forEach(element => {
        const statusText = element.textContent.trim().toLowerCase();
        element.classList.remove("status-waiting", "status-ready", "status-paid"); 

        if (statusText === "в ожидании") {
            element.classList.add("status-waiting");
        } else if (statusText === "готово") {
            element.classList.add("status-ready");
        } else if (statusText === "оплачено") {
            element.classList.add("status-paid");
        }
    });
});


function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute("content");
}

document.addEventListener("DOMContentLoaded", function () {
    const deleteButton = document.querySelector(".js-delete-order-button");
    const modal = document.getElementById("deleteModal");
    const modalOverlay = document.getElementById("modalOverlay");
    const confirmDelete = document.getElementById("confirmDelete");
    const cancelDelete = document.getElementById("cancelDelete");


    if (deleteButton) {
        deleteButton.addEventListener("click", function () {
            modal.style.display = "block";
            modalOverlay.style.display = "block"; // Show overlay
        });
    }

    if (cancelDelete) {
        cancelDelete.addEventListener("click", function () {
            modal.style.display = "none";
            modalOverlay.style.display = "none"; // Hide overlay
        });
    }

    if (confirmDelete) {
        confirmDelete.addEventListener("click", function () {
            const orderElement = document.getElementById("order-info");
            const ORDER_ID = orderElement ? orderElement.dataset.orderId : null;
            
            fetch(DELETE_ORDER_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken":  getCSRFToken(), 
                },
                body: JSON.stringify({ order_id: Number(ORDER_ID) })
            })
            .then(response => response.text())
            .then(data => {
                modal.style.display = "none";
                modalOverlay.style.display = "none"; 
                window.location.href = "https://order-manager-app-nw07.onrender.com/delete_order"
            })
            .catch(error => console.error("Error:", error));
        });
    }; 
});


