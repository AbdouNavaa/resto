from django.db import models

class Coupon(models.Model):
    STATUS_CHOICES = [
        ('مفعل', 'مفعل'),
        ('معطل', 'معطل'),
    ]
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.IntegerField()
    use_number= models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='مفعل')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.code
