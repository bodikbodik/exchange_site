import asyncio
import aiohttp
from asgiref.sync import sync_to_async
from main.models import Crypto

BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/24hr"

# Основна асинхронна функція для отримання даних
async def fetch_crypto_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(BINANCE_API_URL) as response:
            if response.status == 200:
                data = await response.json()

                # Створимо список символів для видалення та дані для оновлення
                symbols_to_delete = []
                crypto_data_to_update = []

                for item in data:
                    symbol = item['symbol']
                    volume_24h = float(item.get('volume', 0))

                    # Якщо об'єм за 24 години = 0, додаємо в список для видалення
                    if volume_24h == 0:
                        symbols_to_delete.append(symbol)
                    else:
                        price = float(item['lastPrice'])
                        market_cap = int(float(item.get('quoteVolume', 0)))
                        high_24h = float(item.get('highPrice', 0))
                        low_24h = float(item.get('lowPrice', 0))
                        change_24h = float(item.get('priceChangePercent', 0))

                        crypto_data_to_update.append({
                            'symbol': symbol,
                            'price': price,
                            'market_cap': market_cap,
                            'volume_24h': volume_24h,
                            'high_24h': high_24h,
                            'low_24h': low_24h,
                            'change_24h': change_24h,
                        })

                # Видалення криптовалют без торгів за 24 години за один запит
                if symbols_to_delete:
                    await delete_cryptos(symbols_to_delete)

                # Оновлення/додавання криптовалют в базу
                for crypto_data in crypto_data_to_update:
                    await update_or_create_crypto(crypto_data)

            else:
                print("Помилка отримання даних з Binance")

# Асинхронне видалення криптовалют
@sync_to_async
def delete_cryptos(symbols):
    Crypto.objects.filter(symbol__in=symbols).delete()
    print(f"Видалено криптовалюти без торгів: {', '.join(symbols)}")

# Асинхронне оновлення або додавання криптовалют
@sync_to_async
def update_or_create_crypto(crypto_data):
    Crypto.objects.update_or_create(
        symbol=crypto_data['symbol'],
        defaults=crypto_data
    )
    print(f"Оновлено/створено: {crypto_data['symbol']}")

# Запуск асинхронної функції
async def main():
    await fetch_crypto_data()

# Для запуску
if __name__ == "__main__":
    asyncio.run(main())
