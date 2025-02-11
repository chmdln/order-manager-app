import pytest
from django.utils import timezone
from django.urls import reverse
from orders.models import Order



@pytest.mark.django_db
def test_search_order_page_renders_correctly(client):
    """Test that the search order page renders correctly on a GET request."""
    
    response = client.get(reverse("search_order"))
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "Введите номер стола или статус заказа" in content  
    assert "Поиск" in content 


@pytest.mark.django_db
def test_search_order_by_table_number(client):
    """Test searching for an order by table number."""
    
    order = Order.objects.create(
        table_number=5, 
        status="оплачено", 
        total_price=100, 
        created_at=timezone.localtime(timezone.now()),
        items={}
    )
    
    response = client.post(reverse("search_order"), data={"search-order": "5"})
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "5" in content  
    assert "оплачено" in content  
    assert "100" in content  



@pytest.mark.django_db
def test_search_order_by_status(client):
    """Test searching for orders by order status."""
    
    order1 = Order.objects.create(
        table_number=1, status="в ожидании", total_price=30, items={}
    )
    order2 = Order.objects.create(
        table_number=2, status="в ожидании", total_price=50, items={}
    )
    order3 = Order.objects.create(
        table_number=3, status="оплачено", total_price=70, items={}
    )
    
    response = client.post(
        reverse("search_order"), 
        data={"search-order": "в ожидании"}
    )
    
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "1" in content  
    assert "2" in content 
    assert "в ожидании" in content  
    assert "оплачено" not in content  




@pytest.mark.django_db
def test_search_order_with_invalid_term(client):
    """Test searching with an invalid search term returns no results."""
    
    response = client.post(
        reverse("search_order"), 
        data={"search-order": "неизвестно"}
    )
    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "*Введите номер стола или статус заказа" in content 



@pytest.mark.django_db
def test_search_order_with_empty_search_renders_all_orders(client):
    """Test empty search renders page with all orders."""
    
    order1 = Order.objects.create(
        table_number=1, status="в ожидании", total_price=30, items={}
    )
    order2 = Order.objects.create(
        table_number=2, status="оплачено", total_price=50, items={}
    )
    
    response = client.post(
        reverse("search_order"), 
        data={"search-order": ""}
    )
    
    assert response.status_code == 200  
    content = response.content.decode("utf-8")
    assert "1" in content
    assert "2" in content
    assert "в ожидании" in content
    assert "оплачено" in content