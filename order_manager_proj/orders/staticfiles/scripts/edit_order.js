const mainMenuButtonSidebar = document.querySelector(".js-main-menu-button-sidebar")
mainMenuButtonSidebar.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:8000'
})


document.addEventListener("DOMContentLoaded", function () {
    const statusButton = document.querySelector(".js-edit-order-status-button");
    const currstOrderStatus = document.querySelector(".curr-order-status");
    const newStatusInput = document.querySelector("#new-order-status");
    newStatusInput.value = "";

    if (statusButton && currstOrderStatus) {
        statusButton.addEventListener("click", function(event) { 
            event.preventDefault(); 
            newStatusInput.value = "";
            currstOrderStatus.style.display = "none";
            statusButton.style.display = "none";

            const newStatusElem = document.querySelector(".curr-order-new-status"); 
            newStatusElem.style.display = "block";
        });
    }; 


    const statusContainer = document.querySelector(".curr-order-status");
    const editStatusButton = document.querySelector(".js-edit-order-status-button");
    const newStatusContainer = document.querySelector(".curr-order-new-status");
    const cancelNewOrderButton = document.querySelector(".js-cancel-new-order-button");
    
    cancelNewOrderButton.addEventListener("click", function (event) {
        event.preventDefault(); 
        statusContainer.innerText = currstOrderStatus.innerText.trim();
        newStatusContainer.style.display = "none";
        statusContainer.style.display = "flex";
        editStatusButton.style.display = "block";

    });
});         
    


document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".curr-order-new-status form");
    const statusInput = document.getElementById("new-order-status");
    const errorNote = document.querySelector(".new-order-status-note");

    if (form) {
        form.addEventListener("submit", function (event) {
            const validStatuses = ["в ожидании", "готово", "оплачено"];
            const inputValue = statusInput.value.trim().toLowerCase();

            if (!validStatuses.includes(inputValue)) {
                event.preventDefault(); 
                errorNote.style.color = "red";
                errorNote.style.display = "block"; 
            } else {
                errorNote.style.display = "none"; 
            }
        });
    }
});




