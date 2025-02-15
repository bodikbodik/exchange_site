(function() {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.async = true;
    script.src = "https://s3.tradingview.com/tv.js";
    document.getElementsByTagName('head')[0].appendChild(script);
  })();
  
  window.addEventListener("load", function() {
    var widget = null;  // Перемінна для графіка
  
    // Функція для оновлення графіка
    window.updateChart = function(symbol) {
      if (widget !== null) {
        widget.remove(); // Видаляємо старий графік
      }
  
      widget = new TradingView.widget({
        "autosize": true,
        "symbol": symbol, // новий символ
        "interval": "D",
        "container_id": "tradingview-widget",
        "theme": "light",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "hide_side_toolbar": false,
        "enable_publishing": false,
        "allow_symbol_change": true,
        "save_image": false
      });
    };
  
    // Ініціалізація графіка за замовчуванням (наприклад, для BTC)
    updateChart("BINANCE:BTCUSDT");
  });
  
  $(document).ready(function() {
    $('table').on('click', '.crypto-row', function() {
      var symbol = $(this).data('symbol'); // Отримуємо символ
      var price = $(this).data('price'); // Отримуємо ціну
      var change = $(this).data('change'); // Отримуємо зміну за 24 години
      var max = $(this).data('max'); // Отримуємо максимальну ціну за 24 години
      var min = $(this).data('min'); // Отримуємо мінімальну ціну за 24 години
      var volume = $(this).data('volume'); // Отримуємо обсяг за 24 години
  
      // Оновлюємо всі елементи в інфо-блоці
      $('#crypto-symbol').text(symbol);
      $('#crypto-price').text("Price: " + price);
      $('#crypto-change').text("Change 24h: " + change);
      $('#crypto-24h-max').text("24h Max: " + max);
      $('#crypto-24h-min').text("24h Min: " + min);
      $('#crypto-volume').text("24h Volume: " + volume);
  
      // Оновлюємо графік
      updateChart(symbol);
    });
  
    // Обробник пошуку
    $('#search').on('input', function() {
      var searchQuery = $(this).val();
  
      // AJAX-запит для оновлення таблиці та пагінації
      $.ajax({
        url: '/crypto/',  // Адреса для обробки пошукового запиту
        data: {
          search: searchQuery,  // Параметр пошуку
          sort: '{{ sort_by }}',  // Параметр сортування
          order: '{{ order }}',  // Параметр напрямку сортування
          page: 1  // Сторінка, яку ми обробляємо
        },
        success: function(data) {
          // Оновлюємо таблицю
          $('.crypto-list-container').html($(data).find('.crypto-list-container').html());
          $('.pagination').html($(data).find('.pagination').html());
  
          // Оновлюємо URL для підтримки пошукового запиту
          window.history.pushState({}, '', '/crypto/?search=' + searchQuery + '&sort={{ sort_by }}&order={{ order }}&page=1');
          
          // Прив'язуємо обробники для кліків на нові елементи таблиці
          bindRowClick();
        }
      });
    });
  
    // Функція для обробки кліків по рядках таблиці
    function bindRowClick() {
      $('table').on('click', '.crypto-row', function() {
        var symbol = $(this).data('symbol'); // Отримуємо символ криптовалюти
        updateChart(symbol); // Оновлюємо графік
  
        // Оновлюємо всі елементи в верхньому блоці
        $('#crypto-symbol').text(symbol);
        $('#crypto-price').text("Price: " + $(this).data('price'));
        $('#crypto-change').text("Change 24h: " + $(this).data('change'));
        $('#crypto-24h-max').text("24h Max: " + $(this).data('max'));
        $('#crypto-24h-min').text("24h Min: " + $(this).data('min'));
        $('#crypto-volume').text("24h Volume: " + $(this).data('volume'));
      });
    }
  
    // Ініціалізація обробників подій для таблиці
    bindRowClick();
  });