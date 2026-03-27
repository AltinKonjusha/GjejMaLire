from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    category = models.CharField(max_length=200, blank=True)
    image_url = models.URLField(blank=True)
    is_tracked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    platform = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='ALL')
    product_url = models.URLField()
    in_stock = models.BooleanField(default=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.platform} - {self.price}"

    class Meta:
        ordering = ['-scraped_at']