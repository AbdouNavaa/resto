from django.conf import settings
from django.db import models
from tables.models import Table

class Order(models.Model):
    STATUS_CHOICES = [
        ('قيد التنفيذ', 'قيد التنفيذ'),
        ('في الطريق', 'في الطريق'),
        ('تم التسليم', 'تم التسليم'),
        ('تم التأكيد', 'تم التأكيد'),
        ('تم الغاء', 'تم الغاء'),
    ]
    
    TYPE_CHOICES = [
        ('dine_in', 'حضور'),
        ('take_out', 'طلب للخارج'),
        ('delivery', 'توصيل'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)  # Optionnel pour 'dine_in'
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='قيد التنفيذ')
    order_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='dine_in')  # Type de commande
    pickup_time = models.DateTimeField(null=True, blank=True)  # Optionnel pour 'take_out'
    delivery_address = models.CharField(max_length=255, null=True, blank=True)  # Optionnel pour 'delivery'
    phone_number = models.CharField(max_length=20, null=True, blank=True)  # Optionnel pour 'delivery'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.id}"