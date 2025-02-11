const mainMenuButtonSidebar = document.querySelector(".js-main-menu-button-sidebar")
mainMenuButtonSidebar.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:8000'
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

function isInvalidInput(input) {
    const validStatuses = new Set(["в ожидании", "готово", "оплачено"]);
    const isInteger = Number.isInteger(Number(input));
    const isValidStatus = validStatuses.has(input.toLowerCase());
    return !isInteger && !isValidStatus;
}

function validateInput() {
    const inputValueElem = document.getElementById("search-order");
    const searchOrderNote = document.querySelector(".search-order-note");
    const valid = isInvalidInput(inputValueElem.value)
    if (valid) {
        searchOrderNote.style.display = 'block'; 
        inputValueElem.value = ""; 
        return false;
    }
    return true; 
}
