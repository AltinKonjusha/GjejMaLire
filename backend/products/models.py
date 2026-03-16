from django.db import models

class Product(models.Model):
    PLATFORM_CHOICES = [
        ('gjirafa50', 'Gjirafa50'),
        ('foleja', 'Foleja'),
        ('neptun', 'Neptun'),
    ]

    name = models.CharField(max_length=500)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(max_length=1000)
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    in_stock = models.BooleanField(default=True)
    last_checked = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('url', 'platform')  # Avoid duplicates

    def __str__(self):
        return f"{self.name} — {self.platform} — {self.current_price}"


class PriceHistory(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='price_history'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scraped_at']

    def __str__(self):
        return f"{self.product.name} — {self.price} @ {self.scraped_at}"


class SearchLog(models.Model):
    query = models.CharField(max_length=500)
    results_count = models.IntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.query}" — {self.results_count} results'