from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from .services import fetch_crypto_data
from .models import Crypto
import requests
import feedparser


def crypto(request):
    # Отримання даних з API і збереження їх у базу
    fetch_crypto_data()

    # Параметри для сортування
    allowed_sort_fields = ['symbol', 'price', 'market_cap', 'volume_24h', 'high_24h', 'low_24h', 'change_24h']
    sort_by = request.GET.get('sort', 'price')  # За замовчуванням сортуємо по 'price'
    order = request.GET.get('order', 'asc')  # За замовчуванням порядок зростання ('asc')

    if sort_by not in allowed_sort_fields:
        sort_by = 'price'  # За замовчуванням сортуємо по 'price'

    if order == 'desc':
        sort_by = f'-{sort_by}'  # Додаємо '-' для зворотного сортування

    # Пошук
    search_query = request.GET.get('search', '')
    cryptos = Crypto.objects.all()

    if search_query:
        cryptos = cryptos.filter(symbol__icontains=search_query)

    # Перевіряємо, чи є в базі дані криптовалюта BTCUSDT
    btc_info = Crypto.objects.filter(symbol="BTCUSDT").first()

    # Сортуємо дані
    cryptos = cryptos.order_by(sort_by)
    
    news = get_crypto_news()
    # Налаштування пагінації (по 10 елементів на сторінку)
    paginator = Paginator(cryptos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Якщо запит є AJAX, відправляємо лише частину таблиці
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'main/crypto.html', {
            'page_obj': page_obj,
            'btc_info': btc_info,
            'sort_by': sort_by,
            'order': order,
            'search_query': search_query,
            
        })

    # Якщо це звичайний запит
    return render(request, 'main/crypto.html', {
        'page_obj': page_obj,
        'btc_info': btc_info,
        'sort_by': sort_by,
        'order': order,
        'search_query': search_query,
        'news': news,
    })


def convert_crypto(request):
    # Отримуємо параметри з запиту
    from_currency = request.GET.get('from_currency')
    to_currency = request.GET.get('to_currency')
    amount = request.GET.get('amount')

    if not from_currency or not to_currency or not amount:
        return JsonResponse({'error': 'Missing required parameters'}, status=400)

    try:
        amount = float(amount)
    except ValueError:
        return JsonResponse({'error': 'Invalid amount'}, status=400)

    # Формуємо символи для запитів до API
    from_symbol = f"{from_currency}"
    to_symbol = f"{to_currency}"

    # Отримуємо дані від API Binance
    try:
        from_response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={from_symbol}')
        to_response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={to_symbol}')
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f"Error fetching data from Binance"})

    # Перевірка статусу відповіді
    if from_response.status_code != 200:
        return JsonResponse({'error': f"Error: First cryptocurrency entered incorrectly "})

    if to_response.status_code != 200:
        return JsonResponse({'error': f"Error: Second cryptocurrency entered incorrectly "})

    # Отримуємо ціну з відповіді API
    try:
        from_data = from_response.json()
        to_data = to_response.json()
    except ValueError:
        return JsonResponse({'error': 'Error parsing JSON response from Binance'})

    # Перевірка, чи є поле 'price' у відповіді
    if 'price' not in from_data or 'price' not in to_data:
        return JsonResponse({'error': 'API response does not contain price data'})

    # Отримуємо ціни криптовалют
    from_price = float(from_data['price'])
    to_price = float(to_data['price'])

    # Конвертуємо кількість
    converted_amount = (amount * from_price) / to_price

    # Повертаємо результат
    return JsonResponse({
        'from_currency': from_currency,
        'to_currency': to_currency,
        'amount': amount,
        'converted_amount': converted_amount,
        'from_price': from_price,
        'to_price': to_price
    })



def get_crypto_news():
    """Отримує останні крипто-новини"""
    rss_url = 'https://cointelegraph.com/rss'
    feed = feedparser.parse(rss_url)
    return feed.entries  # Повертаємо список новин


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
