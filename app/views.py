from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/main.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )

def google_sheets(request):
    """Renders the Google Sheets export page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/google_sheets.html',
        {
            'title': 'Google Sheets Export',
            'year': datetime.now().year,
        }
    )

def competitor_prices(request):
    """Renders the competitor prices page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/competitor_prices.html',
        {
            'title': 'Competitor Prices',
            'year': datetime.now().year,
        }
    )

def niche_analysis(request):
    """Renders the niche analysis page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/niche_analysis.html',
        {
            'title': 'Niche Analysis',
            'year': datetime.now().year,
        }
    )
from .parsing import parse_category
def category_parsing(request):
    """Renders the category parsing page."""
    results = None  # �� ��������� ������ ���

    # ���������, ���� ��� POST-������
    if request.method == 'POST':
        category_url = request.POST.get('category_url')  # �������� ������ �� �����
        if category_url:
            # ����� ������� ��������
            results = parse_category(category_url)

    return render(
        request,
        'app/category_parsing.html',
        {
            'title': 'Category Parsing',
            'year': datetime.now().year,
            'results': results,  # �������� ���������� � ������
        }
    )

import json
from django.shortcuts import render
from django.http import JsonResponse
from .forms import CategoryParsingYandexForm, CategoryParsingLamodaForm
from .yandex_market_parser import parse_yandex_market_category  # Импорт функции парсера
from .parsingwb import parse_category_wb  # Импорт функции парсера
from .lamoda_parser import parse_lamoda_category  # Импорт функции парсера

def category_parsing_wb(request):
    results = None
    error_message = None

    if request.method == "POST":
        form = CategoryParsingYandexForm(request.POST)
        if form.is_valid():
            category_url = form.cleaned_data["category_url"]
            try:
                results = parse_category_wb(category_url)  # Преобразование JSON в Python-объект
            except Exception as e:
                error_message = f"Ошибка при парсинге: {str(e)}"
        else:
            error_message = "Введён некорректный URL."

    else:
        form = CategoryParsingYandexForm()

    return render(request, "app/category_parsing_wb.html", {
        "form": form,
        "products": results,
        "error_message": error_message
    })


def category_parsing_y(request):
    results = None
    error_message = None

    if request.method == "POST":
        form = CategoryParsingYandexForm(request.POST)
        if form.is_valid():
            category_url = form.cleaned_data["category_url"]
            try:
                parsed_data = parse_yandex_market_category(category_url)  # Запуск парсера
                results = json.loads(parsed_data)  # Преобразование JSON в Python-объект
            except Exception as e:
                error_message = f"Ошибка при парсинге: {str(e)}"
        else:
            error_message = "Введён некорректный URL."

    else:
        form = CategoryParsingYandexForm()

    return render(request, "app/category_parsing_y.html", {
        "form": form,
        "results": results,
        "error_message": error_message
    })

from .lamoda_parser import parse_lamoda_category # Import your scraper


def category_parsing_lm(request):
    if request.method == 'POST':
        category_url = request.POST.get('category_url')
        if category_url:
            try:
                products = parse_lamoda_category(category_url)

                # Convert the list of Prod objects to a list of dictionaries
                results = [
                    {
                        'article': p.article,
                        'brand': p.brand,
                        'title': p.title,
                        'price': p.price,
                        'price_old': p.price_old,
                        'price_new': p.price_new,
                        'full_url': p.full_url,
                        'update_date': p.update_date,
                    }
                    for p in products
                ]
                # Option 1: Render with a template (using the list of dictionaries)
                return render(request, 'app/category_parsing_lm.html', {'results': results})

                # Option 2:  Return JSON directly (if you're using AJAX)
                # return JsonResponse({'results': results})


            except Exception as e:
                print(f"Error during parsing: {e}")
                error_message = "Произошла ошибка при парсинге. Пожалуйста, проверьте URL и попробуйте снова."
                return render(request, 'app/category_parsing_lm.html', {'error_message': error_message})
                # Or, for AJAX:  return JsonResponse({'error_message': error_message}, status=500)

    # Handle GET requests (e.g., initial page load)
    return render(request, 'app/category_parsing_lm.html')  # Or return an appropriate response for GET
    # Or, for AJAX: return JsonResponse({})

def sales_predictions(request):
    """Renders the sales predictions page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/sales_predictions.html',
        {
            'title': 'Sales Predictions',
            'year': datetime.now().year,
        }
    )

