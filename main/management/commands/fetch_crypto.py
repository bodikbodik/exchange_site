import asyncio
from django.core.management.base import BaseCommand
from main.services import fetch_crypto_data  # Твоя асинхронна функція для отримання даних

class Command(BaseCommand):
    help = "Fetch cryptocurrency data from Binance API and store in database"

    def handle(self, *args, **kwargs):
        # Виклик асинхронної функції через asyncio
        asyncio.run(self.fetch_data())  # Викликаємо асинхронну функцію через asyncio

    async def fetch_data(self):
        # Викликаємо асинхронну функцію для оновлення даних
        await fetch_crypto_data()  
        self.stdout.write(self.style.SUCCESS("Дані успішно оновлено!"))
