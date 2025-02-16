(function() {
  var script = document.createElement('script');
  script.type = 'text/javascript';
  script.async = true;
  script.src = "https://s3.tradingview.com/tv.js";
  document.getElementsByTagName('head')[0].appendChild(script);
})();

window.addEventListener("load", function() {
  var widget = null;  // Перемінна для графіка
  var defaultSymbol = "BINANCE:BTCUSDT"; // Завжди використовуємо BTCUSDT як дефолт

  // Функція для оновлення графіка
  window.updateChart = function(symbol) {
      if (widget !== null) {
          widget.remove(); // Видаляємо старий графік
      }

      // Додаємо кнопку для відкриття на весь екран в контейнер графіка
      const fullscreenButton = document.createElement("button");
      fullscreenButton.id = "fullscreen-button"; // додаємо id для кнопки
      fullscreenButton.innerHTML = '<i class="fas fa-expand"></i>'; // Іконка для розширення

      // Додаємо кнопку до контейнера графіка
      const container = document.getElementById("tradingview-widget-container");
      container.appendChild(fullscreenButton);

      fullscreenButton.addEventListener("click", () => {
          const chartContainer = document.getElementById("tradingview-widget");
          if (!document.fullscreenElement) {
              chartContainer.requestFullscreen();
              fullscreenButton.innerHTML = '<i class="fas fa-expand"></i>'; // Іконка для виходу з повного екрану
          } else {
              document.exitFullscreen();
              fullscreenButton.innerHTML = '<i class="fas fa-expand"></i>'; // Іконка для входу в повний екран
          }
      });

      widget = new TradingView.widget({
          "autosize": true, // Автоматичне визначення розміру
          "symbol": symbol, // Символ (назва активу)
          "interval": "D", // Інтервал (D - денний графік)
          "container_id": "tradingview-widget", // ID контейнера для виджета
          "theme": "light", // Тема (світла)
          "locale": "en", // Мова інтерфейсу
          "toolbar_bg": "#f1f3f6", // Колір фону тулбара
          "hide_side_toolbar": false, // Приховати бічну панель (false - не ховати)
          "enable_publishing": false, // Дозволити публікацію графіків
          "allow_symbol_change": true, // Дозволити зміну символу
          "save_image": false, // Дозволити збереження зображень
          "studies": [ // Додані індикатори
              "MACD@tv-basicstudies", // MACD
              "RSI@tv-basicstudies"
          ],
          "style": "1", // Стиль графіка (1 - свічковий, 2 - бари, 3 - лінія тощо)
          "timezone": "Etc/UTC", // Часовий пояс
          "withdateranges": true, // Відображення вибору діапазону дат
          "calendar": true, // Відображення економічного календаря
          "hide_top_toolbar": false, // Приховати верхню панель (false - не ховати)
          "range": "12M", // Діапазон графіка (12M - 12 місяців)
          "show_volume": true, // Відображення обсягу торгів
          "width": "100%", // Ширина виджета
          "height": "600", // Висота виджета
          "hideideas": false, // Приховати ідеї користувачів (false - не ховати)
          "studies_overrides": { // Налаштування індикаторів
              "MACD@tv-basicstudies.histogram.color": "#FF0000", // Колір гістограми MACD
              "MACD@tv-basicstudies.signal.color": "#00FF00", // Колір сигнальної лінії MACD
              "RSI@tv-basicstudies.line.color": "#0000FF" // Колір лінії RSI
          }
      });
  };

  // Ініціалізація графіка за замовчуванням (наприклад, для BTC)
  updateChart(defaultSymbol); // Завжди використовуємо дефолтний символ
});

$(document).ready(function() {
  // Перехоплюємо кліки по рядках таблиці
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

  // Обробка пагінації
  $('.pagination').on('click', 'a', function(e) {
      e.preventDefault(); // Скасовуємо стандартну поведінку

      var url = $(this).attr('href'); // Отримуємо URL для нової сторінки
      $.ajax({
          url: url,
          success: function(data) {
              // Оновлюємо таблицю з новими даними
              $('.crypto-list-container').html($(data).find('.crypto-list-container').html());
              $('.pagination').html($(data).find('.pagination').html());

              // Підключаємо обробники подій для нових елементів таблиці
              bindRowClick();
          }
      });
  });
});
