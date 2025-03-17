from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='categories/',default='noimage.jpg')  # Les images seront stockées dans media/dishes/
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
    