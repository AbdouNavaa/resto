from django.db import models
from categories.models import Category

class Dish(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='dishes/')  # Les images seront stockées dans media/dishes/
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        print("Enregistrement de l'image dans :", self.image.path)  # Affiche le chemin complet de l'image
        super().save(*args, **kwargs)
