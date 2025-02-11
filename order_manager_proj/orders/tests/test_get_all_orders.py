import pytest
from django.utils import timezone
from django.urls import reverse
from orders.models import Order, Item
from decimal import Decimal



@pytest.mark.django_db
def test_get_all_orders_page_renders_correctly(client):
    """Test that the page with all orders renders correctly on the frontend."""
    
    item1 = Item.objects.create(name="Домашний лагман", price=30.00)
    item2 = Item.objects.create(name="Чизкейк", price=15.00)
    item3 = Item.objects.create(name="Мороженое Эскимо", price=7.50)

    order1 = Order.objects.create(
        table_number=5, 
        status="оплачено", 
        total_price=75.00, 
        created_at=timezone.localtime(timezone.now()),
        items={str(item1.id): 2, str(item2.id): 1}  
    )

    order2 = Order.objects.create(
        table_number=10, 
        status="готово", 
        total_price=7.50, 
        created_at=timezone.localtime(timezone.now()),
        items={str(item3.id): 1}
    )

    response = client.get(reverse("all_orders"))  
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Создать заказ" in content  
    assert "Чизкейк" in content         
    assert "Домашний лагман" in content
    assert "оплачено" in content       
    assert "готово" in content
    assert "75.00" in content            
    assert "7.50" in content



@pytest.mark.django_db
def test_get_all_orders_empty(client):
    """Test retrieving all orders when there are no orders"""

    response = client.get(reverse("all_orders"))
    assert response.status_code == 200
    assert "orders" in response.context
    assert response.context["orders"] == []



@pytest.mark.django_db
def test_get_all_orders(client):
    """Test retrieving all orders"""

    item1 = Item.objects.create(name="Пицца", price=20.00)
    item2 = Item.objects.create(name="Паста", price=15.95)

    order1 = Order.objects.create(
        table_number=5, 
        status="оплачено", 
        total_price=55.95, 
        created_at=timezone.localtime(timezone.now()),
        items={str(item1.id): 2, str(item2.id): 1}  
    )

    order2 = Order.objects.create(
        table_number=10, 
        status="в ожидании", 
        total_price=15.95, 
        created_at=timezone.localtime(timezone.now()),
        items={str(item2.id): 1}
    )

    response = client.get(reverse("all_orders"))  
    assert response.status_code == 200
    assert "orders" in response.context  

    orders = response.context["orders"]
    assert len(orders) == 2  

    order1_data = next((o for o in orders if o["id"] == order1.id), None)
    assert order1_data is not None
    assert order1_data["table_number"] == 5
    assert order1_data["total_price"] == Decimal("55.95")
    assert order1_data["status"] == "оплачено"
    assert "Пицца" in order1_data["dishes"]
    assert "Паста" in order1_data["dishes"]
    assert order1_data["created_at"] is not None  

    order2_data = next((o for o in orders if o["id"] == order2.id), None)
    assert order2_data is not None
    assert order2_data["table_number"] == 10
    assert order2_data["total_price"] == Decimal("15.95")
    assert order2_data["status"] == "в ожидании"
    assert "Паста" in order1_data["dishes"]
    assert order2_data["created_at"] is not None  