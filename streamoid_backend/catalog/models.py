from django.db import models

class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    mrp = models.IntegerField()
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.sku})"
