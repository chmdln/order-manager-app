const viewAllOrdersButton = document.querySelector(".js-view-all-orders-button")
viewAllOrdersButton.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com/get_all_orders'
})

const createOrderButton = document.querySelector(".js-create-order-button")
createOrderButton.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com/create_order'
})

const searchOrderButtonSidebar = document.querySelector(".js-search-order-button-sidebar")
searchOrderButtonSidebar.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com/search_order'
})

const editOrderButton = document.querySelector(".js-edit-order-button")
editOrderButton.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com/edit_order'
})

const cancelOrderButton = document.querySelector(".js-cancel-order-button")
cancelOrderButton.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com/delete_order'
})

const getRevenueButtonSidebar = document.querySelector(".js-get-revenue-button-sidebar")
getRevenueButtonSidebar.addEventListener('click', () => {
    window.location.href = 'https://order-manager-app-nw07.onrender.com/get_revenue'
})