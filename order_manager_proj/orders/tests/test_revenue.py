import pytest
from django.urls import reverse
from orders.models import Order, Item
from django.utils.timezone import now
import json 



@pytest.fixture
def test_data(db):
    """Fixture to create test items and orders."""
    test_date = now().date()

    item1 = Item.objects.create(name="Круассан с шоколадом", price=10.99)
    item2 = Item.objects.create(name="Кофе", price=5.00)
    item3 = Item.objects.create(name="Пицца", price=20.00)
    item4 = Item.objects.create(name="Паста", price=15.95)

    Order.objects.create(
        table_number=1,
        status="оплачено",
        total_price=15.99,
        items={str(item1.id): 1, str(item2.id): 1},
        created_at=test_date
    )

    Order.objects.create(
        table_number=11,
        status="оплачено",
        total_price=55.95,
        items={str(item3.id): 2, str(item4.id): 1},
        created_at=test_date
    )

    Order.objects.create(
        table_number=20,
        status="в ожидании",
        total_price=31.9,
        items={str(item4.id): 2},
        created_at=test_date
    )
    return test_date



@pytest.mark.django_db
def test_get_revenue_page_renders(client):
    """Test if the revenue page renders correctly."""
    
    response = client.get(reverse("get_revenue"))
    assert response.status_code == 200
    assert "total_revenue" in response.context
    assert "selected_date" in response.context
    assert response.context["total_revenue"] is None
    assert response.context["selected_date"] is None
    
    content = response.content.decode()
    assert "Выберите дату для расчета выручки" in content
    assert "Рассчитать" in content
    assert "Количество заказов" in content
    assert "Общая выручка" in content



@pytest.mark.django_db
def test_get_revenue_valid_date(client, test_data):
    """Test getting revenue for a date with paid orders."""
    
    response = client.post(
        reverse("get_revenue"),
        data=json.dumps({"date": str(test_data)}),
        content_type="application/json"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["orders_number"] == 2
    assert data["revenue"] == 71.94 
    assert data["date"] == test_data.strftime("%d %B %Y")



@pytest.mark.django_db
def test_get_revenue_no_orders(client):
    """Test fetching revenue for a date with no paid orders."""

    response = client.post(
        reverse("get_revenue"),
        data=json.dumps({"date": "2025-01-01"}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["orders_number"] == 0
    assert data["revenue"] == 0
    assert data["date"] == "01 января 2025"
