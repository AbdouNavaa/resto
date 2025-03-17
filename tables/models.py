from django.db import models

class Table(models.Model):
    number = models.IntegerField(unique=True)
    number_of_seats = models.IntegerField(unique=True)
    status = models.CharField(max_length=20, choices=[('متاحة', 'متاحة'), ('محجوزة', 'محجوزة')], default='متاحة')

    def __str__(self):
        return f"Table {self.number}"
