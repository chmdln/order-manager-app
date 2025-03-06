import locale
from datetime import datetime, date
from django.utils.timezone import make_aware, get_current_timezone
from orders.models import Item

def format_date(date_obj):
    # Set Russian locale
    # locale.setlocale(locale.LC_TIME, "ru_RU")
    if isinstance(date_obj, date) and not isinstance(date_obj, datetime):  
        date_obj = datetime.combine(date_obj, datetime.min.time())  # Convert `date` to `datetime`

    if date_obj.tzinfo is None:  # ✅ Ensure the datetime is timezone-aware
        date_obj = make_aware(date_obj, timezone=get_current_timezone())
    return date_obj.strftime("%d %B %Y, %H:%M")  # ✅ "Feb 25, 2025"


def create_order_data(orders): 
    orders_data = []
    for order in orders: 
        data = {
            "id": order.id,
            "table_number": order.table_number,
            "total_price": order.total_price,
            "status": order.status,
            "dishes": [], 
            "created_at": format_date(order.created_at)
        }

        for (item_id, _) in order.items.items(): 
            item = Item.objects.filter(id=item_id).first()
            data["dishes"].append(item.name)
        orders_data.append(data)
    return orders_data