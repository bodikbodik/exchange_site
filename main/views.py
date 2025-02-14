from django.shortcuts import render
from .services import fetch_crypto_data
from .models import Crypto

def crypto(request):
    # Отримання даних з API і збереження їх у базу
    fetch_crypto_data()

    # Отримання усіх криптовалют із бази
    cryptos = Crypto.objects.all()

    # Передача даних у шаблон
    return render(request, 'main/crypto.html', {'cryptos': cryptos})





def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def stocks(request):
    return render(request, 'main/stocks.html')


def funds(request):
    return render(request, 'main/funds.html')

def currency(request):
    return render(request, 'main/currency.html')
