# main/services.py
import requests
from .models import Crypto

def get_crypto_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки
        data = response.json()

        # Фільтруємо пари криптовалют до USDT
        crypto_pairs = [crypto for crypto in data if crypto['symbol'].endswith('USDT')]

        # Зберігаємо дані в базу
        for crypto in crypto_pairs:
            Crypto.objects.update_or_create(
                symbol=crypto['symbol'],
                defaults={
                    'price': crypto['lastPrice'],
                    'volume': crypto['volume'],
                    'high_24h': crypto['highPrice'],
                    'low_24h': crypto['lowPrice'],
                }
            )
    except requests.exceptions.RequestException as e:
        print(f"Помилка запиту до Binance: {e}")


def get_crypto_chart(symbol='BTCUSDT', interval='1m', limit=50):
    """
    Функція для отримання історичних даних про криптовалюту для графіка
    """
    url = f"https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Обробляємо дані для графіка
        history = [{"time": entry[0], "price": entry[4]} for entry in data]

        return history
    except requests.exceptions.RequestException as e:
        print(f"Помилка запиту до Binance: {e}")
        return []
