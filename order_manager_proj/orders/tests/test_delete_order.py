import pytest
from django.urls import reverse
from orders.models import Order, Item
import json 



@pytest.mark.django_db
def test_render_delete_order_item_valid_order(client):
    """
    Test that a valid order ID renders the page 
    with correct order details.
    """

    item1 = Item.objects.create(name="Салат с киноа и лососем", price=14.00)
    item2 = Item.objects.create(name="Паста", price=21.99)

    order = Order.objects.create(
        table_number=3,
        status="оплачено",
        total_price=40.00,
        items={str(item1.id): 1, str(item2.id): 2} 
    )

    response = client.post(
        reverse("render_delete_order_item"),
        data={"order_id": str(order.id)}
    )

    assert response.status_code == 200
    assert "order" in response.context
    assert response.context["order"]["id"] == order.id
    assert response.context["order"]["table_number"] == 3
    assert response.context["order"]["total_price"] == order.total_price
    assert response.context["order"]["status"] == order.status
    assert "Салат с киноа и лососем" in response.context["order"]["dishes"]
    assert "Паста" in response.context["order"]["dishes"]
    assert "orders/delete_order.html" in [t.name for t in response.templates]
    assert "Удалить" in response.content.decode()  



@pytest.mark.django_db
def test_render_delete_order_item_nonexistent_order(client):
    """Test that a non-existent order ID redirects to delete order home."""
    
    response = client.post(
        reverse("render_delete_order_item"),
        data={"order_id": "999999"} 
    )

    assert response.status_code == 200
    assert "orders" in response.context
    assert response.context["orders"] == []


@pytest.mark.django_db
def test_render_delete_order_item_invalid_order_id(client):
    """Test that an invalid (non-numeric) order ID redirects to delete order home."""
    response = client.post(
        reverse("render_delete_order_item"),
        data={"order_id": "invalid_id"}
    )

    assert response.status_code == 200
    assert "orders" in response.context
    assert response.context["orders"] == []



@pytest.mark.django_db
def test_render_delete_order_item_missing_order_id(client):
    """Test that submitting without an order_id redirects to delete order home."""
    
    response = client.post(
        reverse("render_delete_order_item"),
        data={}  
    )

    assert response.status_code == 200
    assert "orders" in response.context
    assert response.context["orders"] == []



@pytest.mark.django_db
def test_delete_order_success(client):
    """Test successful order deletion."""
    
    order = Order.objects.create(
        table_number=1,
        status="в ожидании",
        total_price=20.00,
        items={}
    )

    response = client.post(
        reverse("delete_order"),
        data=json.dumps({"order_id": order.id}),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert not Order.objects.filter(id=order.id).exists()  
    assert "orders" in response.context
    assert response.context["orders"] == []