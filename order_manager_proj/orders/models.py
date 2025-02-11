from django.db import models
from django.utils import timezone



class Item(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=50, 
        verbose_name="Название блюда"
    )
    price = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        verbose_name="Цена")

    def __str__(self): 
        return f"{self.name}"




class Order(models.Model):

    STATUS_CHOICES = [
        ('в ожидании', 'В ожидании'),
        ('готово', 'Готово'), 
        ('оплачено', 'Оплачено'),
    ]

    id = models.AutoField(primary_key=True)
    table_number = models.IntegerField(verbose_name="Номер стола")
    items = models.JSONField(verbose_name="Список блюд с ценами")  
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00, 
        verbose_name="Общая стоимость"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='в ожидании', 
        verbose_name="Статус заказа"
    )
    created_at = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"Order {self.id} - Table {self.table_number}"
    

