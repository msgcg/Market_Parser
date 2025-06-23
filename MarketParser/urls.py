from datetime import datetime
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from app import views  # ����������� views �� ������ ���������� "app"
urlpatterns = [
    # ������� ��������
    path('', views.home, name='home'),
    
    # �����
    path('login/',
         LoginView.as_view(
             template_name='app/login.html',
             extra_context={
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    
    # ������
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    
    # �����-������
    path('admin/', admin.site.urls),
    
    # �������������� ��������
    path('google-sheets/', views.google_sheets, name='google_sheets'),
    path('competitor-prices/', views.competitor_prices, name='competitor_prices'),
    path('niche-analysis/', views.niche_analysis, name='niche_analysis'),
    path('parsing-ozon/', views.category_parsing, name='category_parsing'),
    path('parsing-wildberries/', views.category_parsing_wb, name='category_parsing_wb'),
    path('parsing-yandexmarket/', views.category_parsing_y, name='category_parsing_y'),
    path('parsing-lamoda/', views.category_parsing_lm, name='category_parsing_lm'),
    path('sales-predictions/', views.sales_predictions, name='sales_predictions'),
    
]

