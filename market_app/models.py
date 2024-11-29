from django.db import models


class Market(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    net_worth = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.TextField()
    markets = models.ManyToManyField(Market, related_name='sellers')        # related_name: Name, mit dem wir vom Market darauf zugreifen (ein Seller kann zu mehreren Markets gehören!)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=50, decimal_places=2)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='products')   # ein Product hat nur einen Market! (aber ein Market kann mehrere Products haben!)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')   # ein Product hat nur einen Seller! (aber ein Seller kann mehrere Products haben!)

    def __str__(self):
        return f"{self.name} ({self.price})"
