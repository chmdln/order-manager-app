from django.core.management.base import BaseCommand
from orders.models import Item

class Command(BaseCommand):
    """Command to add a list of items to the database."""
    help = 'Adds a list of items to the database'

    def handle(self, *args: tuple, **kwargs: dict) -> None:
        items_data = [
            {"name": "Бриошь с лососем", "price": 10.0},
            {"name": "Грин салат", "price": 15.0},
            {"name": "Салат с киноа и лососем", "price": 20.0},
            {"name": "Салат с курицей", "price": 15.0},
            {"name": "Салат с курицей и беконом", "price": 16.99},
            {"name": "Пельмени китайские жареные", "price": 24.50},
            {"name": "Домашний лагман", "price": 30.00},
            {"name": "Спринг роллы с курицей и сыром 4 шт", "price": 10.00},
            {"name": "Фри с мясом", "price": 27.50},
            {"name": "Фри с курицей", "price": 24.00},
            {"name": "Чизкейк", "price": 15.00}, 
            {"name": "Мороженое Эскимо", "price": 7.50}, 
            {"name": "Кофе", "price": 2.00}, 
            {"name": "Bubble Tea Strawberry", "price": 1.50}   
        ]
        
        for item_data in items_data:
            Item.objects.create(**item_data)

