# models.py
from django.db import models

class Crypto(models.Model):
    symbol = models.CharField(max_length=20, unique=True)  # Символ криптовалюти (наприклад, BTCUSDT)
    price = models.DecimalField(max_digits=20, decimal_places=8)  # Поточна ціна
    volume = models.DecimalField(max_digits=20, decimal_places=8)  # Обсяг торгів
    high_24h = models.DecimalField(max_digits=20, decimal_places=8)  # Найвища ціна за 24 години
    low_24h = models.DecimalField(max_digits=20, decimal_places=8)  # Найнижча ціна за 24 години
    last_updated = models.DateTimeField(auto_now=True)  # Час оновлення даних

    def __str__(self):
        return str(self.symbol)
