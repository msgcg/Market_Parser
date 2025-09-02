# Market Parser

Проект представляет собой веб-парсер на Django для сбора данных о товарах с различных маркетплейсов, таких как Ozon, Wildberries, Lamoda и Яндекс.Маркет.

## 🚀 Возможности

-   **Парсинг нескольких платформ**: Поддержка Ozon, Wildberries (обычные и цифровые товары), Lamoda и Яндекс.Маркет.
-   **Веб-интерфейс**: Удобный интерфейс на Django для запуска парсинга по URL категории.
-   **Обход защиты**: Использование `selenium-stealth` для обхода систем защиты от ботов.
-   **Сохранение данных**: Результаты сохраняются в файлы формата `.xlsx` для дальнейшего анализа.
-   **Обработка пагинации**: Автоматическая прокрутка и переход по страницам для сбора всех товаров из категории.
-   **Уведомления в Telegram**: Интеграция с Telegram-ботом для отправки отладочной информации и статусов парсинга.
-   **Инкрементальное обновление**: При повторном парсинге данные в Excel-файлах обновляются, а не дублируются, на основе URL товара и даты обновления.

## 🛠️ Стек технологий

-   **Backend**: Python, Django
-   **Парсинг**: Selenium, BeautifulSoup4, Requests
-   **Работа с данными**: openpyxl
-   **Уведомления**: python-telegram-bot

## ⚙️ Установка и запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/msgcg/Market_Parser.git
    cd Market_Parser
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Настройте переменные окружения:**
    -   **Telegram-уведомления**: В файле `app/telegram_debugger.py` замените плейсхолдеры `YOUR_TELEGRAM_BOT_TOKEN` и `YOUR_TELEGRAM_CHAT_ID` на ваши реальные данные.
    ```python
    # app/telegram_debugger.py
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
    ```
    -   **(Опционально) Google Sheets**: Если вы планируете использовать выгрузку в Google Таблицы (в данный момент код закомментирован), вам понадобится:
        -   Файл `credentials.json` от сервисного аккаунта Google Cloud. Поместите его в корневую папку проекта.
        -   В файле `app/parsing.py` раскомментируйте код, связанный с Google Sheets, и укажите ваш `SPREADSHEET_ID`.

5.  **Установите ChromeDriver:**
    Для работы Selenium требуется ChromeDriver, версия которого должна соответствовать версии вашего браузера Google Chrome. Скачайте его с официального сайта и убедитесь, что он доступен в системном `PATH`, или укажите путь к нему в коде (например, в файле `app/parsing.py` в функциях `init_webdriver`).

6.  **Примените миграции и запустите сервер Django:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

7.  **Откройте приложение в браузере:**
    Перейдите по адресу `http://127.0.0.1:8000/`.

## 📂 Структура проекта

```
Market_Parser/
├── app/                  # Django-приложение парсера
│   ├── migrations/
│   ├── static/
│   ├── templates/        # HTML-шаблоны
│   │   └── app/
│   ├── __init__.py
│   ├── forms.py          # Формы Django
│   ├── lamoda_parser.py  # Логика парсинга Lamoda
│   ├── models.py
│   ├── parsing.py        # Логика парсинга Ozon
│   ├── parsingwb.py      # Логика парсинга Wildberries
│   ├── parsingwb_digital.py # Логика парсинга цифровых товаров WB
│   ├── telegram_debugger.py # Модуль для отправки сообщений в Telegram
│   ├── tests.py
│   ├── views.py          # Контроллеры (представления)
│   └── yandex_market_parser.py # Логика парсинга Яндекс.Маркет
├── MarketParser/         # Настройки проекта Django
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── parsed_data/          # Папка для сохранения результатов (создается автоматически)
│   ├── lamoda/
│   ├── ozon/
│   ├── wb/
│   └── yandex/
├── manage.py             # Утилита для управления Django
└── requirements.txt      # Список зависимостей
```

## 📝 Использование

-   Перейдите на главную страницу.
-   Выберите нужный маркетплейс из меню.
-   Вставьте URL категории, которую хотите спарсить, в соответствующее поле.
-   Нажмите кнопку для запуска парсинга.
-   Результаты будут сохранены в `.xlsx` файл в папке `parsed_data`. Первые 100 результатов будут также отображены на странице.
