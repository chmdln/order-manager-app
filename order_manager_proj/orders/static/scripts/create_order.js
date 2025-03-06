document.addEventListener("DOMContentLoaded", function () {
    
    const select = document.getElementById("table_number");
    const maxTables = 20; // Change this if you need more tables

    for (let i = 1; i <= maxTables; i++) {
        const option = document.createElement("option");
        option.value = i;
        option.textContent = i;
        select.appendChild(option);
    }
}); 


const mainMenuButtonSidebar = document.querySelector(".js-main-menu-button-sidebar")
mainMenuButtonSidebar.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com'
})


function validateForm() {
    let valid = false;
    document.querySelectorAll('[name^="quantity_"]').forEach(function(input) {
        if (input.value && input.value >= 1) {
            valid = true;
        }
    });
    
    if (!valid) {
        alert("Please select at least one menu item.");
        return false;  
    }
    return true;  
}








