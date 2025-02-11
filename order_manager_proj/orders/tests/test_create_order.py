import pytest
from django.urls import reverse
from orders.models import Order, Item
from decimal import Decimal



@pytest.mark.django_db
def test_create_order_form_renders(client):
    """Test that the create order form renders correctly."""
    
    Item.objects.create(name="Круассан с шоколадом", price=10.99)
    Item.objects.create(name="Кофе", price=5.00)

    response = client.get(reverse("create_order"))
    assert response.status_code == 200
    assert "orders/order_form.html" in [t.name for t in response.templates]
    assert "menu" in response.context
    assert len(response.context["menu"]) == 2
    content = response.content.decode("utf-8")
    assert "<h1>Создать заказ</h1>" in content  
    assert 'name="table_number"' in content  
    assert 'name="quantity_' in content  
    assert "Круассан с шоколадом" in content  
    assert "Кофе" in content



@pytest.mark.django_db
def test_create_order_valid(client):
    """Test creating an order with valid data."""

    item1 = Item.objects.create(name="Пицца", price=20.00)
    item2 = Item.objects.create(name="Паста", price=15.95)

    data = {
        "table_number": "5",
        f"quantity_{item1.id}": "2",  
        f"quantity_{item2.id}": "1"   
    }

    response = client.post(reverse("create_order"), data, follow=True)
    assert response.status_code == 200  
    assert response.redirect_chain[-1][0] == reverse("all_orders")  
    order = Order.objects.first()
    assert order is not None
    assert order.table_number == 5
    assert order.items == {str(item1.id): 2, str(item2.id): 1}
    assert order.total_price == Decimal("55.95")



@pytest.mark.django_db
def test_create_order_no_items(client):
    """Test creating an order without selecting any items."""
    Item.objects.create(name="Салат", price=7.50)

    data = {
        "table_number": "3",
    }

    response = client.post(reverse("create_order"), data)
    assert response.status_code == 302  
    assert Order.objects.count() == 0