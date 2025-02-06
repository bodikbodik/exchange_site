# main/services.py
import requests

def get_crypto_data(page=1, per_page=10):
    """
    Функція для отримання даних криптовалют з Binance API
    і повернення криптовалют на заданій сторінці.
    """
    url = "https://api.binance.com/api/v3/ticker/24hr"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Фільтруємо пари криптовалют до USDT
        crypto_pairs = [crypto for crypto in data if crypto['symbol'].endswith('USDT')]

        total_cryptos = len(crypto_pairs)  # Загальна кількість криптовалют
        total_pages = max(1, (total_cryptos + per_page - 1) // per_page)

        # Розбиваємо на сторінки
        start = (page - 1) * per_page
        end = start + per_page
        paginated_cryptos = crypto_pairs[start:end]

        return paginated_cryptos, total_pages
    except requests.exceptions.RequestException as e:
        print(f"Помилка запиту до Binance: {e}")
        return [], 0


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
