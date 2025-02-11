import pytest
from django.urls import reverse
from orders.models import Order, Item



@pytest.mark.django_db
def test_render_order_for_edit_get_request(client):
    """Test GET request renders the edit order home page with no orders."""
    
    response = client.get(reverse("edit_order"))
    assert response.status_code == 200
    assert "orders" in response.context
    assert response.context["orders"] == []



@pytest.mark.django_db
def test_render_order_for_edit_post_empty_order_id(client):
    """Test POST request with empty order_id renders edit order home page."""
    
    response = client.post(
        reverse("edit_order"), 
        data={"order_id": ""}
    )
    assert response.status_code == 200
    assert "orders" in response.context
    assert response.context["orders"] == []



@pytest.mark.django_db
def test_render_order_for_edit_post_valid_order_id(client):
    """Test POST request with a valid order_id renders the order edit page with correct order details."""

    item1 = Item.objects.create(name="Пицца", price=20.00)
    item2 = Item.objects.create(name="Паста", price=15.95)

    order = Order.objects.create(
        table_number=3,
        status="готово",
        total_price=40.00,
        items={str(item1.id): 2, str(item2.id): 1} 
    )

    response = client.post(
        reverse("edit_order"),
        data={"order_id": str(order.id)}
    )

    assert response.status_code == 200
    assert "orders/edit_order.html" in [t.name for t in response.templates]
    assert "order" in response.context
    
    order_context = response.context["order"]
    assert order_context["id"] == order.id
    assert order_context["table_number"] == 3
    assert order_context["status"] == "готово"
    assert float(order_context["total_price"]) == 40.00
    assert "Пицца" in order_context["dishes"]
    assert "Паста" in order_context["dishes"]

    content = response.content.decode("utf-8")
    assert f"ID Заказа :</span> {order.id}</div>" in content  
    assert "готово" in content 
    assert "40.00" in content 
    assert "Пицца" in content
    assert "Паста" in content



@pytest.mark.django_db
def test_render_order_for_edit_post_invalid_order_id(client):
    """Test POST request with a non-numeric order_id"""

    response = client.post(
        reverse("edit_order"),
        data={"order_id": "invalid_id"}
    )
    # Django converts BadRequest to HTTP 400
    assert response.status_code == 400  


@pytest.mark.django_db
def test_render_order_for_edit_post_nonexistent_order_id(client):
    """Test POST request with a non-existent order_id returns 400 Bad Request."""
    
    response = client.post(
        reverse("edit_order"),
        data={"order_id": "999999"} 
    ) 
    assert response.status_code == 400



@pytest.mark.django_db
def test_edit_order_status_valid(client):
    """Test updating an order's status successfully."""
    
    order = Order.objects.create(
        table_number=2,
        status="в ожидании",
        total_price=50.00,
        items={}
    )

    response = client.post(
        reverse("edit_order_status"),
        data={"order_id": str(order.id), "new_order_status": "готово"}
    )

    order.refresh_from_db()
    assert response.status_code == 200
    assert order.status == "готово" 
    assert "order" in response.context  
    assert response.context["order"]["status"] == "готово"



@pytest.mark.django_db
def test_edit_order_status_missing_order_id(client):
    """
    Test submitting without an order_id 
    should render the edit order home page.
    """
    
    response = client.post(
        reverse("edit_order_status"),
        data={"new_order_status": "готово"}  
    )

    assert response.status_code == 200
    assert "orders" in response.context  
    assert response.context["orders"] == []  



@pytest.mark.django_db
def test_edit_order_status_empty_status(client):
    """
    Test submitting an empty new_order_status 
    should not change the order status.
    """
    
    order = Order.objects.create(
        table_number=5,
        status="готово",
        total_price=30.00,
        items={}
    )

    response = client.post(
        reverse("edit_order_status"),
        data={"order_id": str(order.id), "new_order_status": ""}  
    )

    order.refresh_from_db()
    
    assert response.status_code == 200
    assert "order" in response.context
    assert response.context["order"]["status"] == ""
    content = response.content.decode("utf-8")
    assert '*Введите "в ожидании", "готово" или "оплачено"' in content 


