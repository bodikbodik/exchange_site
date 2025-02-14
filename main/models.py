from django.db import models

class Crypto(models.Model):
    symbol = models.CharField(max_length=30, unique=True, default="")  # Наприклад, BTC, ETH
    name = models.CharField(max_length=50, default="Unknown")  # Повна назва: Bitcoin, Ethereum (дефолтне значення)
    price = models.DecimalField(max_digits=20, decimal_places=10, default=0.0)  # Ціна
    market_cap = models.BigIntegerField(default=0)  # Ринкова капіталізація
    volume_24h = models.BigIntegerField(default=0)  # Об'єм торгів за 24 години
    circulating_supply = models.BigIntegerField(default=0)  # Монет в обігу
    total_supply = models.BigIntegerField(null=True, blank=True, default=None)  # Загальна емісія
    max_supply = models.BigIntegerField(null=True, blank=True, default=None)  # Максимальна емісія
    change_24h = models.FloatField(default=0.0)  # Зміна ціни за 24 години
    high_24h = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True, default=None)  # Макс ціна за 24 години
    low_24h = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True, default=None)  # Мін ціна за 24 години
    last_updated = models.DateTimeField(auto_now=True)  # Час оновлення
    
    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.price}$"
