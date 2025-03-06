const mainMenuButtonSidebar = document.querySelector(".js-main-menu-button-sidebar")
mainMenuButtonSidebar.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com'
})


function getRevenue() {
    let selectedDate = document.getElementById("calendar").value;
    if (!selectedDate) {
        alert("Выберите дату!");
        return;
    }

    fetch("/get_revenue/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({ date: selectedDate }),
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(".revenue-item-date span").textContent = data.date;
        document.querySelector(".revenue-item-orders-number span").textContent = data.orders_number;
        document.querySelector(".revenue-item-total span").textContent = `${data.revenue} руб.`; 
    })
    .catch(error => console.error("Ошибка:", error));
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


document.addEventListener("DOMContentLoaded", function () {
    flatpickr("#calendar", {
        enableTime: false,  
        inline: true,
        dateFormat: "Y-m-d", 
        locale: "ru", 
    });
});


