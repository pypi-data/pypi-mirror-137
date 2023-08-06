from django.urls import path
from .views import cash_register_login_view, cash_register_logout, cash_register_view, getCartItems, cartBtns
from django.conf import settings


if 'DJANGO_CASH_REGISTER_MAIN_PAGE' in dir(settings):
    django_cash_register_url = ''
else:
    django_cash_register_url = 'django_cash_register/'


urlpatterns = [
    path(django_cash_register_url, cash_register_view),
    path(f'{django_cash_register_url}logout/', cash_register_logout),
    path(f'{django_cash_register_url}login/', cash_register_login_view, name='django_cash_register_login'),
    path(f'{django_cash_register_url}ajax/getCartItems/', getCartItems, name='getCartItems'),
    path(f'{django_cash_register_url}ajax/cartBtns/', cartBtns, name='cartBtns'),
]
