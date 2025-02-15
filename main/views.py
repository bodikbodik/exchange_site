from django.shortcuts import render
from django.core.paginator import Paginator
from .services import fetch_crypto_data
from .models import Crypto

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
    })











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
