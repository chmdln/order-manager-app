from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import BadRequest
from django.utils.dateparse import parse_date
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 

from decimal import Decimal
from typing import Dict, Optional 
from datetime import date 
import json 

from ..models import Item, Order
from .utils import format_date, create_order_data


def ping(request: HttpRequest) -> HttpResponse:
    response = HttpResponse(status=200)
    response["Content-Length"] = "0"
    return response 


def main(request: HttpRequest) -> HttpResponse:
    """
    Main view. Renders the main menu.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the main menu rendered.
    """
    return render(
        request=request,
        template_name="orders/main_menu.html",
        context={}
    )



def get_all_orders(request: HttpRequest) -> HttpResponse:
    """
    Get all orders. Renders the orders_all.html template with the context containing all orders.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the orders_all.html template rendered.
    """
    orders: list[Order] = Order.objects.all()
    orders_data = create_order_data(orders)

    response = render(
        request=request, 
        template_name="orders/orders_all.html", 
        context={"orders": orders_data}
    )
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response



def create_order(request: HttpRequest) -> HttpResponse: 
    """
    Handles order creation.

    If the request is a POST, it retrieves the table number and the quantities of each item
    in the order. It then creates an Order object with the table number, items, and total price.
    If the request is a GET, it retrieves the menu items and renders the order_form.html template
    with the context containing the menu items.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the order_form.html template rendered
            or a redirect to the all_orders page.
    """
    if request.method == "POST":
        table_number = request.POST.get("table_number")

        items: Dict[int, int] = {}
        total_price = Decimal(0)
        
        for item in Item.objects.all():
            quantity = request.POST.get(f"quantity_{item.id}")
            if quantity:
                items[item.id] = int(quantity)
                total_price += (item.price * int(quantity))

        if not items:
            messages.error(request, "Вы должны добавить хотя бы одно блюдо.")
            return redirect("create_order")  
        
        order = Order.objects.create(
            table_number=table_number,
            items=items,
            total_price=total_price
        )
        return redirect("all_orders") 

    menu = Item.objects.all()
    return render(
        request=request, 
        template_name="orders/order_form.html", 
        context={"menu": menu}
    )



def search_order(request: HttpRequest) -> HttpResponse:
    """
    Handles order search by table number of order status.

    If the request is a POST, it retrieves the search term.
    If the search term is a number, it filters orders by table number.
    If the search term is a string, it filters orders by status.
    If the search term is empty, it renders all orders.
    If the request is a GET, it renders all orders.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the orders_all.html template rendered.
    """
    if request.method == "POST":
        search_term = request.POST.get("search-order")
        if search_term.isdigit():
            orders = Order.objects.filter(table_number=search_term)
            orders_data = create_order_data(orders)
            return render(
                request=request, 
                template_name="orders/orders_all.html", 
                context={"orders": orders_data}
            )
        elif isinstance(search_term, str):
            statuses = {"в ожидании", "готово", "оплачено"}
            search_term = search_term.lower()
            if search_term in statuses: 
                orders = Order.objects.filter(status=search_term)
                orders_data = create_order_data(orders)
                return render(
                    request=request, 
                    template_name="orders/orders_all.html", 
                    context={"orders": orders_data}
                )
        elif not search_term:
            return redirect("all_orders")
        
    orders = Order.objects.all()
    orders_data = create_order_data(orders)
    return render(
        request=request, 
        template_name="orders/orders_all.html", 
        context={"orders": orders_data}
    )



def render_order_by_id(
        request: HttpRequest, 
        order_id: int, 
        template_name: str
) -> HttpResponse: 
    """
    Utility function: Renders a template with the order data
    by the given order ID.

    Args:
        request (HttpRequest): The HTTP request object.
        order_id (int): The ID of the order to render.
        template_name (str): The name of the template to render.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    order = Order.objects.filter(id=order_id).first() 
    if order: 
        data = {
            "id": order.id,
            "table_number": order.table_number,
            "total_price": order.total_price,
            "status": order.status,
            "dishes": []
        }
        for (item_id, quantity) in order.items.items(): 
            item = Item.objects.filter(id=item_id).first()
            data["dishes"].append(item.name)

        return render(
            request=request,
            template_name=template_name,
            context={"order": data}
        ) 
    raise BadRequest(
        "Order with id {} does not exist".format(order_id)
    )
    


def render_order_for_edit(request: HttpRequest) -> HttpResponse:
    """
    Handles order edit by retrieving the order ID from the request and 
    redirecting to the order edit page if the ID is valid.

    If the request is a POST, it retrieves the order ID from the request.
    If the order ID is valid, it renders the order edit page with the order data.
    If the order ID is empty, it renders the order edit home page 
    with an empty list of orders.

    If the request is a GET, it renders the order edit home page with an empty 
    list of orders.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    if request.method == "POST":
        if not request.POST.get("order_id"):
            return render(
                request=request, 
                template_name="orders/edit_order_home.html", 
                context={"orders": []}
            )
        
        order_id = request.POST.get("order_id")
        if order_id.isdigit():
            return render_order_by_id(
                request=request, 
                order_id=int(order_id), 
                template_name="orders/edit_order.html")
        
        raise BadRequest(
            "Invalid input. Order id must be a number"
        )
    
    return render(
        request=request, 
        template_name="orders/edit_order_home.html", 
        context={"orders": []}
    )



def edit_order_status(request: HttpRequest) -> HttpResponse:
    """
    Handles updating the status of an order.

    If the request is a POST, it retrieves the order ID and new status from the request.
    If the order ID is valid and the order exists, it updates the order's status and renders
    the order edit page with the updated order status. If the request is not a POST or the
    order does not exist, it renders the order edit home page with an empty list of orders.

    Args:
        request (HttpRequest): The HTTP request object containing order ID and new status.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order = Order.objects.filter(id=order_id).first()
        if order:
            new_status = request.POST.get("new_order_status").strip().lower()
            order.status = new_status
            order.save()
            return render_order_by_id(
                request=request,
                order_id=order_id,
                template_name="orders/edit_order.html"
            )

    return render(
        request=request,
        template_name="orders/edit_order_home.html",
        context={"orders": []}
    )



def render_delete_order_item(request: HttpRequest) -> HttpResponse:
    """
    Handles rendering the delete order page.

    If the request is a POST, it retrieves the order ID from the request.
    If the order ID is valid and the order exists, it renders the delete order page
    with the order information. If the request is not a POST or the order does not
    exist, it renders the delete order home page with an empty list of orders.

    Args:
        request (HttpRequest): The HTTP request object containing order ID.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    if request.method == "POST":
        if not request.POST.get("order_id") or not request.POST.get("order_id").isdigit():
            return render(
                request=request, 
                template_name="orders/delete_order_home.html", 
                context={"orders": []}
            )
        
        order_id = int(request.POST.get("order_id"))
        order = Order.objects.filter(id=order_id).first() 
        if order: 
            return render_order_by_id(
                request=request, 
                order_id=order_id,
                template_name="orders/delete_order.html"
            )
    return render(
        request=request, 
        template_name="orders/delete_order_home.html", 
        context={"orders": []}
    )



def delete_order(request: HttpRequest) -> HttpResponse:
    """
    Handles deleting an order by its ID.

    If the request is a POST, it retrieves the order ID from the request body.
    If the order ID is valid and the order exists, it deletes the order and renders
    the delete order home page with an empty list of orders. 

    Args:
        request (HttpRequest): The HTTP request object containing order ID.

    Returns:
        HttpResponse: The HTTP response with the rendered template.
    """
    
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data.get("order_id")
        order = Order.objects.filter(id=order_id).first() 
        if order: 
            order.delete() 
            return render(
                request=request, 
                template_name="orders/delete_order_home.html", 
                context={"orders": []}
            ) 
                     
    return render(
        request=request, 
        template_name="orders/delete_order_home.html", 
        context={"orders": []}
    )



@csrf_exempt
def get_revenue(request: HttpRequest) -> HttpResponse:
    """
    Processes a request to calculate and return the revenue for a specific date.

    If the request method is POST, it retrieves the date from the request body and parses it.
    It then filters orders with status "оплачено" for the specified date to calculate the
    number of orders and total revenue. The result is returned as a JSON response containing
    the formatted date, number of orders, and total revenue.

    Args:
        request (HttpRequest): The HTTP request object containing the date.

    Returns:
        HttpResponse: JSON response with revenue details or a rendered template.
    """

    total_revenue: Optional[float] = None
    selected_date: Optional[str] = None

    if request.method == "POST":
        data = json.loads(request.body)
        selected_date = data.get("date")
        parsed_date: Optional[date] = parse_date(selected_date)

        if parsed_date:
            orders = Order.objects.filter(
                status="оплачено",
                created_at__date=parsed_date
            )
            
            num_of_orders = orders.count()
            total_revenue = orders.aggregate(Sum("total_price"))["total_price__sum"] or 0
         
            return HttpResponse(
                json.dumps({
                    "date": format_date(parsed_date).split(",")[0],
                    "orders_number": num_of_orders,
                    "revenue": float(total_revenue),
                }),
                content_type="application/json"
            )

    return render(
        request=request,
        template_name="revenue.html",
        context={
            "total_revenue": total_revenue,
            "selected_date": selected_date
        }
    )

