from django.core.paginator import Paginator

from django.shortcuts import render
from django.http import JsonResponse
from .services import get_crypto_data, get_crypto_chart


def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def stocks(request):
    return render(request, 'main/stocks.html')



def crypto(request):
    # Отримуємо номер сторінки, або встановлюємо 1 за замовчуванням
    page_number = request.GET.get('page', 1)
    crypto_data, total_pages = get_crypto_data(page=int(page_number))

    # Створюємо Paginator для пагінації
    paginator = Paginator(crypto_data, 10)  # 10 криптовалют на сторінку
    page = paginator.get_page(page_number)

    return render(request, 'main/crypto.html', {
        'paginated_cryptos': page,
        'total_pages': total_pages,
    })

def crypto_chart(request):
    # Отримуємо дані для графіка
    symbol = request.GET.get('crypto', 'BTCUSDT')  # Отримуємо параметр криптовалюти
    history = get_crypto_chart(symbol)
    return JsonResponse({'history': history})

def funds(request):
    return render(request, 'main/funds.html')

def currency(request):
    return render(request, 'main/currency.html')
